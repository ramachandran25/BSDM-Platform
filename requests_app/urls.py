from django.urls import path
from .views import create_request, dashboard, my_requests, request_detail


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('new/', create_request, name='create_request'),
    path('my/', my_requests, name='my_requests'),
    path('<str:request_id>/', request_detail, name='request_detail'),
]
