from django.urls import path
from .views import admin_dashboard, admin_request_detail

urlpatterns = [
    path('', admin_dashboard, name='project_admin_dashboard'),
    path('request/<str:request_id>/', admin_request_detail, name='project_admin_request_detail'),
]
