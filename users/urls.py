from django.urls import path
from .views import UserLogoutView, UserRegisterView, UserLoginView, send_reset_link, reset_password

urlpatterns = [
    path('register/', UserRegisterView, name='register'),
    path('login/',UserLoginView,name='login'),
    path('logout/',UserLogoutView,name='logout'),
    path('send-reset-link/',send_reset_link,name='send-reset'),
    path('reset-pass/<str:token>',reset_password,name='reset-password'),
]
