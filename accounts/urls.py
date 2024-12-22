from django.urls import path,include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('',include('django.contrib.auth.urls')),
    path('register',views.register_view,name='register'),
]
