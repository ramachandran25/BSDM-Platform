from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'mobile_number',
            'college_name',
            'department',
            'dob',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "An account with this email already exists. "
                "Please contact the administrator or use the password reset option."
            )

        return email
