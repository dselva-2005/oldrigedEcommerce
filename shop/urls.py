from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('feedback/', views.feedback, name='feedback'),
    path("contactus/", views.contact_us, name="contact_us"),
    path("payment_methods", views.payment_methods, name="payment_methods"),
    path("delivery", views.delivery, name="delivery"),
    path("return_exch", views.return_exch, name="return_exch"),
    path('search/', views.post_search, name='post_search'),
    path('shop/', views.product_list, name='product_list'),
    path('product/review/', views.review_form,name='product_review'),
    path('<int:id>/<slug:slug>/', views.product_detail,name='product_detail'),
    path('<slug:category_slug>/', views.product_list,name='product_list_by_category'),
]
