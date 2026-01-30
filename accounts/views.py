from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .profile_forms import ProfileForm

from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Registration successful. Please login.'
            )
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user)

    return render(
        request,
        'accounts/profile.html',
        {'form': form}
    )

@require_POST
def save_theme(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "ignored"}, status=200)

    data = json.loads(request.body)
    theme = data.get("theme", "system")

    user = request.user
    user.profile_theme = theme
    user.save(update_fields=["profile_theme"])

    return JsonResponse({"status": "ok"})
