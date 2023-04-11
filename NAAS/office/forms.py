from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from office.models import (
    User,
    ProductList,
    Customer,
    SubscriptionList,
    CustomerRequest,
)

class ManagerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("name", "username")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 0
        if commit:
            user.save()
        return user

class AddDeliveryPersonForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("name", "username")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 1
        user.deliveries = 0
        user.salary = 0
        if commit:
            user.save()
        return user

class AddProductForm(forms.ModelForm):
    class Meta:
        model = ProductList
        fields = ("name", "code", "price", "date_published")
    
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'The Times of India'
        self.fields['code'].widget.attrs['placeholder'] = 'TOA'
        self.fields['price'].widget.attrs['placeholder'] = '300'
        self.fields['date_published'].widget.attrs['placeholder'] = 'MM/DD/YYYY'

class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "username", "address")
    
    def __init__(self, *args, **kwargs):
        super(AddCustomerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'John Doe'
        self.fields['username'].widget.attrs['placeholder'] = 'johndoe121'
        self.fields['address'].widget.attrs['placeholder'] = '221B Baker Street'
    
class AddSubscriptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionList
        fields = ("product",)

    def __init__(self, *args, **kwargs):
        super(AddSubscriptionForm, self).__init__(*args, **kwargs)
        self.fields["product"].empty_label = None

class AddCustomerRequestForm(forms.ModelForm):
    class Meta:
        model = CustomerRequest
        fields = ("customer", "request")
    
    def __init__(self, *args, **kwargs):
        super(AddCustomerRequestForm, self).__init__(*args, **kwargs)
        self.fields["customer"].empty_label = None