from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from office.models import (
    User,
    ProductList,
    Customer,
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
        fields = ["name", "username"]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 1
        if commit:
            user.save()
        return user

class AddProductForm(forms.ModelForm):
    class Meta:
        model = ProductList
        fields = ("name", "date_published")
    
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Product Name'
        self.fields['date_published'].widget.attrs['placeholder'] = 'MM/DD/YYYY'

class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "address")
    
    def __init__(self, *args, **kwargs):
        super(AddCustomerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Customer\'s Name'
        self.fields['address'].widget.attrs['placeholder'] = 'Customer\'s Address'