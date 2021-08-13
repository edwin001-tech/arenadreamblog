from django import forms
from .models import Signup


class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "name": "email",
        "id": "email",
        "class":"form-field",
        "placeholder": "Type your email address",
    }), label="")

    class Meta:
        model = Signup
        fields = ('email', )
