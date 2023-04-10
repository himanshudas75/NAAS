from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import ListView
from office.models import ProductList

def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == 0:
            return redirect('manager:home')
    return redirect('accounts/login/')

class ListProductView(ListView):
    model = ProductList
    ordering = ('id', )
    context_object_name = 'products'
    template_name = 'products.html'