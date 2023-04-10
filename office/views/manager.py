from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from office.models import (
    User,
    ProductList,
    Customer,
    SubscriptionList
)
from django.urls import reverse, reverse_lazy
from office.forms import (
    ManagerSignUpForm,
    AddDeliveryPersonForm,
    AddProductForm,
    AddCustomerForm,
    AddSubscriptionForm,
)
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

class AddDeliveryPersonView(LoginRequiredMixin, CreateView):
    model = User
    form_class = AddDeliveryPersonForm
    template_name = 'manager/item_add.html'
    success_url = reverse_lazy('manager:delivery-persons')

    def get_context_data(self, **kwargs):
        kwargs['item'] = 'Delivery Person'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        return super().form_valid(form)

class ListDeliveryPersonView(LoginRequiredMixin, ListView):
    model = User
    ordering = ('id', )
    context_object_name = 'objects'
    template_name = 'items.html'

    def get_context_data(self, **kwargs):
        kwargs['item'] = 'Delivery Person'
        kwargs['type'] = 'manager:delivery-persons'
        kwargs['add'] = 'manager:delivery-person-add'
        kwargs['delete'] = 'manager:delivery-person-delete'
        return super().get_context_data(**kwargs)

class DeleteDeliveryPersonView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'manager/item_confirm_delete.html'
    success_url = reverse_lazy('manager:delivery-persons')

    def get_context_data(self, **kwargs):
        kwargs['type'] = 'manager:delivery-persons'
        return super().get_context_data(**kwargs)
    
    def test_func(self):
        dp = self.get_object()
        if self.request.user.user_type == 0 and dp.user_type != 0:
            return True
        return False

class AddProductView(LoginRequiredMixin, CreateView):
    model = ProductList
    template_name = 'manager/item_add.html'
    form_class = AddProductForm
    success_url = reverse_lazy('products')

    def get_context_data(self, **kwargs):
        kwargs['item'] = 'Product'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        return super().form_valid(form)

class DeleteProductView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProductList
    template_name = 'manager/item_confirm_delete.html'
    success_url = reverse_lazy('products')

    def get_context_data(self, **kwargs):
        kwargs['type'] = 'products'
        return super().get_context_data(**kwargs)
    
    def test_func(self):
        if self.request.user.user_type == 0:
            return True
        return False

class AddCustomerView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Customer
    template_name = 'manager/item_add.html'
    form_class = AddCustomerForm
    success_url = reverse_lazy('manager:customers')

    def get_context_data(self, **kwargs):
        kwargs['item'] = 'Customer'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.user_type == 0:
            return True
        return False

class ListCustomerView(LoginRequiredMixin, ListView):
    model = Customer
    ordering = ('id', )
    context_object_name = 'objects'
    template_name = 'items.html'

    def get_context_data(self, **kwargs):
        kwargs['item'] = 'Customer'
        kwargs['type'] = 'manager:customers'
        kwargs['add'] = 'manager:customer-add'
        kwargs['delete'] = 'manager:customer-delete'
        return super().get_context_data(**kwargs)

class DeleteCustomerView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Customer
    template_name = 'manager/item_confirm_delete.html'
    success_url = reverse_lazy('manager:customers')

    def get_context_data(self, **kwargs):
        kwargs['type'] = 'manager:customers'
        return super().get_context_data(**kwargs)
    
    def test_func(self):
        if self.request.user.user_type == 0:
            return True
        return False

class ListSubscriptionView(LoginRequiredMixin, CreateView, ListView):
    model = SubscriptionList
    context_object_name = 'objects'
    form_class = AddSubscriptionForm
    template_name = 'manager/subscriptions.html'

    def get_success_url(self):         
        return reverse_lazy('manager:subscriptions', kwargs = {'pk': self.object.customer_id.id})
    
    def form_valid(self, form):
        form.instance.customer_id = Customer.objects.filter(id=self.kwargs['pk']).first()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        kwargs['item'] = 'Customer'
        kwargs['type'] = 'manager:customers'
        kwargs['add'] = 'manager:subscription-add'
        kwargs['delete'] = 'manager:subscription-delete'
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        customer = get_object_or_404(Customer, id=self.kwargs['pk'])
        return self.model.objects.filter(customer_id = customer)

class DeleteSubscriptionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SubscriptionList
    template_name = 'manager/subscription_confirm_delete.html'
    context_object_name = 'object'

    def get_success_url(self):         
        return reverse_lazy('manager:subscriptions', kwargs = {'pk': self.object.customer_id.id})
    
    def test_func(self):
        if self.request.user.user_type == 0:
            return True
        return False

