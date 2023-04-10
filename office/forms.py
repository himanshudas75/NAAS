from django import forms
from django.contrib.auth.forms import UserCreationForm
from office.models import (User, )

class ManagerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["name", "username", "email"]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 0
        if commit:
            user.save()
        print(user)
        return user