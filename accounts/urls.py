from django.urls import path
from .views import register, profile, save_theme


urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path("theme/save/", save_theme, name="save_theme"),
]
