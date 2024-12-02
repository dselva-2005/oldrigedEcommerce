from django.shortcuts import render,get_object_or_404
from .models import OrderItem,Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created,payment_completed
from django.contrib import messages
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseBadRequest,JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        
        if form.is_valid() and cart.get_total_price() != 0 :
            mode = form.cleaned_data['payment_mode']
            # order id of newly created order.
            order = form.save(commit=False)
            order.save()
        
            for item in cart:
                OrderItem.objects.create(order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'])
            # clear the cart
            cart.clear()
            amount = int(cart.get_total_price()*100)
            if mode == 'ONLINE_PAYMENT':
                razorpay_order = razorpay_client.order.create({
                'amount': amount,  # Razorpay accepts amount in paise
                'currency': 'INR',
                'payment_capture': '0',  # 0 for manual capture
                'notes': {'order_id': order.id}  # Optional custom note
                })

                razorpay_order_id = razorpay_order['id']
                callback_url = request.build_absolute_uri(reverse('paymenthandler'))

                # we need to pass these details to frontend.
                context = {}
                context['razorpay_order_id'] = razorpay_order_id
                context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
                context['razorpay_amount'] = amount
                context['currency'] = "INR"
                context['callback_url'] = callback_url
                context['order_id'] = order.id

                return render(request, 'orders/order/payment.html', context=context)

            else:
                order_created.delay(order.id)
                payment_completed.delay(order.id)
                messages.success(request,'Your order is placed successfully')
                return render(request,
                'orders/order/created.html',
                {'order': order})
        
        else:
            if cart.get_total_price() == 0:
                messages.error(request,"Cart is empty checkout is disabled")
            return render(request,
            'orders/order/create.html',
            {'cart': cart, 'form': form})
        
    else:
        if cart.get_total_price() == 0:
                messages.error(request,"Cart is empty checkout is disabled")
        form = OrderCreateForm({'first_name':'dselva',
                                'last_name':'jagan',
                                'email':'dselvajagan@gmail.com',
                                'address':'example',
                                'postal_code':'3223443',
                                'city':'mumbai'})
        return render(request,
        'orders/order/create.html',
        {'cart': cart, 'form': form})



@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                payorder = razorpay_client.payment.fetch(payment_id)
                amount = payorder['amount']
                order_id = payorder['notes']['order_id']
                order = Order.objects.get(id=order_id)
                order.paid = True
                order.online_order_id = payment_id
                order.save()
                order_created.delay(order.id)
                payment_completed.delay(order_id)
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    # render success page on successful caputre of payment
                    return redirect('shop:home')
                except:
                    # if there is an error while capturing payment.
                    return JsonResponse({'status':'error'})
            else:

                # if signature verification fails.
                return redirect('shop:home')
        except:

            # if we don't find the required parameters in POST data
            return redirect('shop:home')
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    


@staff_member_required
def admin_order_detail(request, order_id):
 order = get_object_or_404(Order, id=order_id)
 return render(request,
 'admin/orders/order/detail.html',
 {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
 order = get_object_or_404(Order, id=order_id)
 html = render_to_string('orders/order/pdf.html',{'order': order})
 response = HttpResponse(content_type='application/pdf')
 response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
 weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.BASE_DIR / 'static/css/pdf.css')])
 return response