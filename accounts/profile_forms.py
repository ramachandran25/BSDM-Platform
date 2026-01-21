from django import forms
from .models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'mobile_number',
            'college_name',
            'department',
            'dob',
        )

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'})
        }
