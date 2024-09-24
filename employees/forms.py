from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PersonalDetails


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    usable_password = None

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class EditProfileForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.NumberInput)
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'new-password'}),
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'confirm-new-password'}),
    )

    class Meta:
        model = PersonalDetails
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
        ]

    # Override the form's initialization to set required=False for every field
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        # Check if the new passwords match
        if new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', 'Passwords do not match.')
