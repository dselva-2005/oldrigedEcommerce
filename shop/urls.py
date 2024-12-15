from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('feedback/', views.feedback, name='feedback'),
    path('search/', views.post_search, name='post_search'),
    path('shop/', views.product_list, name='product_list'),
    path('contact/', views.contact_page, name='contact_page'),
    path('policies/', views.policies_page, name='policies_page'),
    path('product/review/', views.review_form,name='product_review'),
    path('<int:id>/<slug:slug>/', views.product_detail,name='product_detail'),
    path('<slug:category_slug>/', views.product_list,name='product_list_by_category'),
]
