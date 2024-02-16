# myapp/forms.py

from django import forms
from .models import Idea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'description']  # Exclude 'creator' and 'votes' as they are handled separately


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']