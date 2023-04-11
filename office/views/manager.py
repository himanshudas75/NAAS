from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from office.models import (
    User,
    ProductList,
    Customer,
    SubscriptionList,
    DeliveryList,
    Bill,
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
        # kwargs['temp'] = 0
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_type = 1)

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
        return reverse_lazy('manager:subscriptions', kwargs = {'pk': self.object.customer.id})
    
    def form_valid(self, form):
        form.instance.customer = Customer.objects.filter(id=self.kwargs['pk']).first()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        kwargs['item'] = 'Customer'
        kwargs['type'] = 'manager:customers'
        kwargs['add'] = 'manager:subscription-add'
        kwargs['delete'] = 'manager:subscription-delete'
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        customer = get_object_or_404(Customer, id=self.kwargs['pk'])
        return self.model.objects.filter(customer = customer)

class DeleteSubscriptionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SubscriptionList
    template_name = 'manager/subscription_confirm_delete.html'
    context_object_name = 'object'

    def get_success_url(self):         
        return reverse_lazy('manager:subscriptions', kwargs = {'pk': self.object.customer.id})
    
    def test_func(self):
        if self.request.user.user_type == 0:
            return True
        return False

class DeliveryListView(LoginRequiredMixin, ListView):
    model = DeliveryList
    template_name = 'delivery_list.html'
    context_object_name = 'object'

    def get_success_url(self):
        if self.request.user.user_type == 0:
            return reverse_lazy('manager:delivery-list')
        return reverse_lazy('delivery-list')

    def get_queryset(self):
        if self.request.user.user_type == 0:
            return self.model.objects.all()
        return self.model.objects.filter(deliveryperson = self.request.user)


def generate_delivery_list(request):
    if DeliveryList.objects.all():
        return redirect('manager:delivery-list')
    dp_list = User.objects.filter(user_type=1)
    dp_len = len(dp_list)
    customer_list = Customer.objects.all()
    customer_len = len(customer_list)

    if customer_len == 0 or dp_len == 0:
        return redirect('manager:delivery-list')

    customers_per_dp = customer_len // dp_len

    start = 0
    for dp in dp_list:
        for i in range(start, min(start+customers_per_dp, customer_len)):
            obj = DeliveryList()
            obj.deliveryperson = dp
            obj.customer = customer_list[i]
            obj.save()
        start = start+customers_per_dp

    for i in range(start, customer_len):
        obj = DeliveryList()
        obj.deliveryperson = dp
        obj.customer = customer_list[i]
        obj.save()
        
    return redirect('manager:delivery-list')

def delete_delivery_list(request):
    DeliveryList.objects.all().delete()
    return redirect('manager:delivery-list')

# ON DELIVERY COMPLETE
# 1. Update deliverylist
# 2. Add the price to deliveries in User table
# 3. Add the Bill to customer
# 4. Update customer due_date by 1

def complete_delivery(request, id):
    # Updating deliverylist
    delivery = DeliveryList.objects.filter(id=id).first()
    delivery.completed = True
    delivery.save()

    # Adding the price
    dp = User.objects.filter(id=delivery.deliveryperson.id).first()
    subscriptions = SubscriptionList.objects.filter(customer=delivery.customer)
    price = 0
    for item in subscriptions:
        price += item.product.price
    dp.deliveries += price
    dp.save()

    # Updating the bill
    bills = Bill.objects.filter(customer=delivery.customer)
    subscriptions = SubscriptionList.objects.filter(customer=delivery.customer)
    if bills:
        for item in subscriptions:
            temp = bills.filter(product=item.product)
            if temp:
                temp = temp.first()
                temp.quantity += 1
            else:
                temp = Bill()
                temp.customer = delivery.customer
                temp.product = item.product
                temp.quantity = 1
            temp.save()
    else:
        for item in subscriptions:
            temp = Bill()
            temp.customer = delivery.customer
            temp.product = item.product
            temp.quantity = 1
            temp.save()
    
    # Update customer due date
    customer = delivery.customer
    customer.due_days += 1
    customer.save()

    return redirect('delivery-list')

def calculate_salary(request):
    delivery = User.objects.filter(user_type=1)
    for dp in delivery:
        dp.salary = dp.deliveries*2.5
        dp.deliveries = 0
        dp.save()
    return redirect('manager:delivery-persons')

# GENERATE PDF HERE
def generate_bill(request, id):
    bills = Bill.objects.filter(customer=id)
    print("AMOUNT PAYABLE: ", end="")
    amount = 0
    if bills:
        for bill in bills:
            amount += bill.product.price * bill.quantity
    print(amount)
    return redirect('manager:customers')

