from django.shortcuts import redirect, render
from django.views.generic import TemplateView

def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == 0:
            return redirect('manager/')
    return redirect('accounts/login/')