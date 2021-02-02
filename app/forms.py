from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Comment

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'post']                  

class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']        