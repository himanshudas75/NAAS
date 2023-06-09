from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView
from office.models import (
    User,
    ProductList,
    Customer,
    SubscriptionList,
    DeliveryList,
    Bill,
    CustomerRequest,
)
from django.urls import reverse_lazy
from office.forms import (
    ManagerSignUpForm,
    AddDeliveryPersonForm,
    AddProductForm,
    AddCustomerForm,
    AddSubscriptionForm,
    AddCustomerRequestForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime, timedelta
import random

def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == 0:
            return render(request, 'home.html')
        elif request.user.user_type == 1:
            return render(request, 'home.html')
    return redirect('login')

class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = 'registration/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('manager:home')

class AddDeliveryPersonView(LoginRequiredMixin, CreateView):
    model = User
    form_class = AddDeliveryPersonForm
    template_name = 'item_add.html'
    success_url = reverse_lazy('manager:delivery-persons')

    def get_context_data(self, **kwargs):
        kwargs['item'] = 'Delivery Person'
        kwargs['title'] = 'Add Delivery Person'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        return super().form_valid(form)

class ListDeliveryPersonView(LoginRequiredMixin, ListView):
    model = User
    ordering = ('id', )
    context_object_name = 'objects'
    template_name = 'items.html'

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Delivery Persons'
        kwargs['item'] = 'Delivery Person'
        kwargs['type'] = 'manager:delivery-persons'
        kwargs['add'] = 'manager:delivery-person-add'
        kwargs['delete'] = 'manager:delivery-person-delete'
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_type = 1)

class DeleteDeliveryPersonView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'item_confirm_delete.html'
    success_url = reverse_lazy('manager:delivery-persons')

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Confirm Delete'
        kwargs['type'] = 'manager:delivery-persons'
        return super().get_context_data(**kwargs)
    
    def test_func(self):
        dp = self.get_object()
        if self.request.user.user_type == 0 and dp.user_type != 0:
            return True
        return False

class AddProductView(LoginRequiredMixin, CreateView):
    model = ProductList
    template_name = 'item_add.html'
    form_class = AddProductForm
    success_url = reverse_lazy('products')

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Add Product'
        kwargs['item'] = 'Product'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        return super().form_valid(form)

class ListProductView(ListView):
    model = ProductList
    ordering = ('id', )
    context_object_name = 'objects'
    template_name = 'items.html'

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Products'
        kwargs['item'] = 'Product'
        kwargs['type'] = 'products'
        kwargs['add'] = 'manager:product-add'
        kwargs['delete'] = 'manager:product-delete'
        return super().get_context_data(**kwargs)
    
class DeleteProductView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProductList
    template_name = 'item_confirm_delete.html'
    success_url = reverse_lazy('products')

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Confirm Delete'
        kwargs['type'] = 'products'
        return super().get_context_data(**kwargs)
    
    def test_func(self):
        if self.request.user.user_type == 0:
            return True
        return False

class AddCustomerView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Customer
    template_name = 'item_add.html'
    form_class = AddCustomerForm
    success_url = reverse_lazy('manager:customers')

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Add Customer'
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
        kwargs['title'] = 'Customers'
        kwargs['item'] = 'Customer'
        kwargs['type'] = 'manager:customers'
        kwargs['add'] = 'manager:customer-add'
        kwargs['delete'] = 'manager:customer-delete'
        return super().get_context_data(**kwargs)

class DeleteCustomerView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Customer
    template_name = 'item_confirm_delete.html'
    success_url = reverse_lazy('manager:customers')

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Confirm Delete'
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
    template_name = 'subscriptions.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'customer_id': self.kwargs['pk']})
        return kwargs
    
    def get_success_url(self):         
        return reverse_lazy('manager:subscriptions', kwargs = {'pk': self.object.customer.id})
    
    def form_valid(self, form):
        form.instance.customer = Customer.objects.filter(id=self.kwargs['pk']).first()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Subscriptions'
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
    template_name = 'subscription_confirm_delete.html'
    context_object_name = 'object'

    def get_success_url(self):         
        return reverse_lazy('manager:subscriptions', kwargs = {'pk': self.object.customer.id})
    
    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Confirm Delete'
        return super().get_context_data(**kwargs)
    
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

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Delivery List'
        if self.request.GET.get("message"):
            kwargs['messages'] = [self.request.GET.get("message")]
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        if self.request.user.user_type == 0:
            return self.model.objects.all()
        return self.model.objects.filter(deliveryperson = self.request.user)

# GENERATE DELIVERY LIST BASED ON FILTERS
# 1. customer should be in subscription list
# 2. pause = 0 for the customer
def generate_delivery_list(request):
    if DeliveryList.objects.all():
        return redirect('manager:delivery-list')
    dp_list = User.objects.filter(user_type=1)
    dp_len = len(dp_list)
    ids = list(SubscriptionList.objects.all().values_list('customer', flat=True).distinct())
    # print("LIST ->", ids)
    customer_list = Customer.objects.filter(id__in=ids, pause=0)
    # print("LIST2 ->", customer_list)
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
# 5. Update customer amount payable
def complete_delivery(request, id):
    # Updating deliverylist
    delivery = DeliveryList.objects.filter(id=id).first()
    delivery.completed = True
    delivery.save()

    # Adding the price to deliveries
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
    
    # Update customer due date and amount payable
    customer = delivery.customer
    customer.due_days += 1
    customer.amount_payable += price
    customer.save()

    # Delete customer if due_days greater than 60
    if customer.due_days > 60:
        customer.delete()
        response = redirect('delivery-list')
        response['Location'] +=f'?message=The customer {customer.username} has been removed for excessive due date'
        return response
    
    return redirect('delivery-list')

def calculate_salary(request):
    delivery = User.objects.filter(user_type=1)
    for dp in delivery:
        dp.salary = dp.deliveries*2.5*0.01
        dp.deliveries = 0
        dp.save()
    return redirect('manager:delivery-persons')

def generate_bill(request, id):
    bills = Bill.objects.filter(customer=id)
    customer = Customer.objects.filter(id=id).first()

    context_dic = {
        'type': 'Bill' if customer.due_days < 30 else 'Reminder',
        'bill_number': random.randint(0, 5000),
        'current_date': datetime.now() + timedelta(hours=5.5),
        'object': bills,
        'amount_payable': customer.amount_payable,
    }

    template = get_template('bill_reminder.html')
    html = template.render(context_dic)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if pdf:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f"Bill_{customer.username}"
        content = f"attachment; filename={filename}.pdf"
        response['Content-Disposition'] = content
        return response
    return None

def pause(request, id, pause):
    customer = Customer.objects.filter(id=id).first()
    if pause:
        customer.pause = 1
    else:
        customer.pause = 0
    customer.save()
    return redirect('manager:customers')

class PaymentGatewayView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'payment.html'
    context_object_name = 'object'
    success_url = reverse_lazy('payment-gateway')

    def get_queryset(self):
        return self.model.objects.filter(id=self.kwargs['id'])
    
def payment(request, id):
    customer = Customer.objects.filter(id=id).first()
    customer.amount_payable = 0
    customer.due_days = 0
    customer.save()

    Bill.objects.filter(customer=customer).delete()

    return redirect('delivery-list')

class ListCustomerRequestsView(LoginRequiredMixin, ListView):
    model = CustomerRequest
    template_name = 'customer_request.html'
    context_object_name = 'objects'
    
    def get_success_url(self):
        if self.request.user.user_type == 0:
            return reverse_lazy('manager:customer-requests')
        return reverse_lazy('customer-requests')
    
    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Customer Requests'
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        if self.request.user.user_type == 0:
            return self.model.objects.all()
        return self.model.objects.filter(deliveryperson = self.request.user)
    
class AddCustomerRequestView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomerRequest
    template_name = 'item_add.html'
    form_class = AddCustomerRequestForm
    success_url = reverse_lazy('customer-requests')

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Add Customer Request'
        kwargs['item'] = 'Request'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        form.instance.deliveryperson = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.user_type == 1:
            return True
        return False

def complete_customer_request(request, id):
    CustomerRequest.objects.filter(id=id).delete()
    return redirect('manager:customer-requests')