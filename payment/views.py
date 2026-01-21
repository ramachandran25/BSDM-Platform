from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def payment_home(request):
    return render(request, 'payment/payment_home.html')
