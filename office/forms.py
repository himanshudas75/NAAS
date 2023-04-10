from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from office.models import (
    User,
    ProductList,
    Customer,
    SubscriptionList
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
        if commit:
            user.save()
        return user

class AddProductForm(forms.ModelForm):
    class Meta:
        model = ProductList
        fields = ("name", "price", "date_published")
    
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'The Times of India'
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
        fields = ("customer_id", "product_id")