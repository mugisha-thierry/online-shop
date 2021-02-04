from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,OrderItem, Order, Transaction,Product, Category, Comment, Rate,Delivery
from django.contrib.auth import login, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import SignUpForm, UpdateUserProfileForm,CommentForm,RateForm,DeliveryForm
from .decorators import admin_only,allowed_users
from django.contrib import messages

import datetime
# import stripe

# Create your views here.
# @login_required(login_url='login')
def home(request):
    object_list = Product.objects.all()
    categorys = Category.get_category()
    return render(request, 'home.html',{'object_list':object_list,'categorys':categorys})

def search_product(request):
    categorys = Category.get_category()
    if 'searchproject' in request.GET and request.GET["searchproject"]:
        search_term = request.GET.get("searchproject")
        searched_project = Product.search_by_name(search_term)
        message = f"{search_term}"
        context = {'object_list':searched_project,'message': message,'categorys':categorys}

        return render(request, "search.html",context)
    else:
      message = "You haven't searched for any term"
      return render(request, 'search.html',{"message":message})     


def search_products(request):
    categorys = Category.get_category()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    if 'searchproduct' in request.GET and request.GET["searchproduct"]:
        search_term = request.GET.get("searchproduct")
        searched_project = Product.search_by_name(search_term)
        message = f"{search_term}"
        context = {'object_list':searched_project,'message': message,'categorys':categorys,'current_order_products': current_order_products,}

        return render(request, "searching.html",context)
    else:
      message = "You haven't searched for any term"
      return render(request, 'searching.html',{"message":message})       

def product_category(request, category):
    object_list = Product.filter_by_category(category)
    categorys = Category.get_category()
    context = {'object_list':object_list,'categorys': categorys}
    return render(request,'category/notlogged.html',context)

# @login_required(login_url='login')
def comment(request, pk):
    image = get_object_or_404(Product, pk=pk)

    product = Product.objects.get(id = pk)
    rates = Rate.objects.order_by('-date')
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = image
            comment.user = request.user.profile
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()

    if request.method == 'POST':
        form_rate = RateForm(request.POST)
        if form_rate.is_valid():
            test = form_rate.cleaned_data['test']
            price = form_rate.cleaned_data['price']
            durability = form_rate.cleaned_data['durability']
            rate = Rate()
            rate.product = image
            rate.user = current_user
            rate.test = test
            rate.price = price
            rate.durability = durability
            rate.average = (rate.test + rate.price + rate.durability)/3
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form_rate = RateForm()    
    context = {
        'image': image,
        'form': form,
        'form_rate':form_rate,
        'rates':rates,
        'product':product,
    }

    return render(request, 'product.html', context)

    

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)
            messages.info(request, "Your account has been Created successfully.")
            return redirect("/login")
    else:
        form = SignUpForm()
    return render(request, 'register/register.html', {'form': form}) 

def profile(request, username):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    if request.method == 'POST':
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return redirect(request.path_info)
    else:
        prof_form = UpdateUserProfileForm(instance=request.user.profile)

    context = {
        'prof_form': prof_form,
        'my_orders':my_orders,

    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def product_list(request):
    object_list = Product.objects.all()
    categorys = Category.get_category()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products,
        'categorys':categorys
    }

    return render(request, "products/product_list.html", context)

def products_category(request, category):
    object_list = Product.filter_by_category(category)
    categorys = Category.get_category()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]
    context = {'object_list':object_list,'categorys': categorys,'current_order_products':current_order_products}
    return render(request,'category/logedin.html',context)     

def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this product
    # if product in request.user.profile.ebooks.all():
    #     messages.info(request, 'You already own this ebook')
    #     return redirect(reverse('product_list')) 
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = 221
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('product_list'))


@login_required(login_url='login')
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('order_summary'))


@login_required(login_url='login')
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'shopping_cart/order_summary.html', context)


@login_required(login_url='login')
def checkout(request, **kwargs):
    client_token = 222
    current_user = request.user
    existing_order = get_user_pending_order(request)
    publishKey = 111
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.save()
            clear_from_cart(request)
            return redirect('product_list')
    else:
        form = DeliveryForm()
            
    context = {
        'order': existing_order,
        'client_token': client_token,
        'form':form,
    }

    return render(request, 'shopping_cart/checkout.html', context)








@login_required(login_url='login')
def clear_from_cart(request):
    current_user = request.user
    cat = get_object_or_404(Order, owner=current_user.id)
    cat.delete()
    messages.info(request, "Thanks for shopping with us")
    return redirect('product_list')     

def admin_page(request):
    return render(request,'admin_page.html')

def about(request):
    return render(request,'about.html')