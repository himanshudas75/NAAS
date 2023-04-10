from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from office.models import User, ProductList
from django.urls import reverse, reverse_lazy
from office.forms import ManagerSignUpForm, AddDeliveryPersonForm, AddProductForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('manager:home')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class HomeView(LoginRequiredMixin, ListView):
    template_name = 'home.html'

    def get_queryset(self):
        return 0

class AddDeliveryPerson(LoginRequiredMixin, CreateView):
    model = User
    form_class = AddDeliveryPersonForm
    template_name = 'manager/delivery_person_add.html'
    success_url = reverse_lazy('manager:add-delivery-person')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'delivery person'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        return super().form_valid(form)

class AddProductView(LoginRequiredMixin, CreateView):
    model = ProductList
    template_name = 'manager/product_add.html'
    form_class = AddProductForm
    success_url = reverse_lazy('manager:add-product')

    def form_valid(self, form):
        return super().form_valid(form)

class DeleteProductView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProductList
    template_name = 'manager/product_confirm_delete.html'
    success_url = reverse_lazy('products')

    def test_func(self):
        if self.request.user.user_type == 0:
            return True
        return False

class ListDeliveryPersonView(LoginRequiredMixin, ListView):
    model = User
    ordering = ('id', )
    context_object_name = 'delivery_persons'
    template_name = 'manager/delivery_persons.html'

class DeleteDeliveryPersonView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'manager/delivery_person_confirm_delete.html'
    success_url = reverse_lazy('manager:delivery-persons')

    def test_func(self):
        dp = self.get_object()
        if self.request.user.user_type == 0 and dp.user_type != 0:
            return True
        return False