from django import forms

from .models import * 

class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = NewUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password"
        )
    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password: 
            raise forms.ValidationError('password does not match')