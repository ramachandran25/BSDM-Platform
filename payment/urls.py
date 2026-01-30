from django.urls import path
from .views import payment_home

urlpatterns = [
    path('', payment_home, name='payment_home'),
]
