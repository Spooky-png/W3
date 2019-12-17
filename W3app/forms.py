from django import forms
from .models import User, Fighter

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name','alias','email','desc','password','picture')