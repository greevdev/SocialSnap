from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['password2'].widget.attrs.update({'autocomplete': 'off'})

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        elif len(password1) > 50:
            raise forms.ValidationError("Password must be less than 50 characters long.")

        return password1

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
