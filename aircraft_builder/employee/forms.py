from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Employee

class EmployeeSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Employee
        fields = ['username', 'email', 'password1', 'password2', 'team']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Employee.objects.filter(email=email).exists():
            raise ValidationError("Bu email adresi zaten kullanımda.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
