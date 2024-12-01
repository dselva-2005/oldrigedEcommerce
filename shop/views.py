from django.shortcuts import render,get_object_or_404
from .models import Product,Category
from cart.forms import CartAddProductForm
# Create your views here.

def product_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=category)

    return render(request,'shop/product/list.html',
                            {'category': category,
                            'categories': categories,
                            'products': products,
                            'cart_product_form': cart_product_form})

def product_detail(request, id, slug):
 product = get_object_or_404(Product,
 id=id,
 slug=slug,
 available=True)
 return render(request,
 'shop/product/detail.html',
 {'product': product})


def home(request):
   try:
        products = Product.objects.all()[5]
   except IndexError:
        products = Product.objects.all()

   return render(request,'shop/home.html',{'products':products})