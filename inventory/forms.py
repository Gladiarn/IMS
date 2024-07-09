from typing import Any
from django.contrib.auth.forms import UserCreationForm
from .models import Order, CustomUser
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'usertype']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'id': 'password1'})
        self.fields['password2'].widget.attrs.update({'id': 'password2'})
        self.fields['username'].widget.attrs.update({'id': 'username'})
        self.fields['usertype'].widget.attrs.update({'id': 'usertype'})
        self.fields['password1'].widget = forms.TextInput(attrs={'type': 'text'})
        self.fields['password2'].widget = forms.TextInput(attrs={'type': 'text'})


class CustomerCreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'usertype']

    def __init__(self, *args, **kwargs):
        super(CustomerCreateUserForm, self).__init__(*args, **kwargs)
        self.fields['usertype'].widget = forms.HiddenInput()  # Hide usertype field for customer signup
        self.fields['usertype'].initial = 'customer'  # Set default usertype to 'customer'
        self.fields['password1'].widget.attrs.update({'id': 'password1'})
        self.fields['password2'].widget.attrs.update({'id': 'password2'})
        self.fields['username'].widget.attrs.update({'id': 'username'})
        self.fields['usertype'].widget.attrs.update({'id': 'usertype'})

    def clean_usertype(self):
        usertype = self.cleaned_data['usertype']
        if usertype != 'customer':
            raise forms.ValidationError("Invalid user type for this form.")
        return usertype