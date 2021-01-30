from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
# from .models import  Profile,Neighbourhood,Neighbourhood_infrastructure,Post
from django.contrib.auth import login, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import SignUpForm, UpdateUserProfileForm,CommentForm
# from .models import  Profile,Neighbourhood,Neighbourhood_infrastructure,Post,Comment
from .decorators import admin_only,allowed_users

# Create your views here.
# @login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)
            return redirect("/")
    else:
        form = SignUpForm()
    return render(request, 'register/register.html', {'form': form}) 