from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, UpdateView
from office.models import User, ProductList
from office.forms import ManagerSignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class HomeView(LoginRequiredMixin, ListView):
    template_name = 'home.html'

    def get_queryset(self):
        return 0

class AddProductView(LoginRequiredMixin, CreateView):
    model = ProductList
    template_name = 'registration/signup.html'
    fields = ['name', 'date_published']
    success_url = '/manager/add_product'

    def form_valid(self, form):
        return super().form_valid(form)


