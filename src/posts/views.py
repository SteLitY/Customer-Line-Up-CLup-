from django.http import HttpResponse
from .models import *
from .forms import CustomerSignUpForm, BusinessSignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from posts.forms import CustomerSignUpForm

# Create your views here.

#CRUD Create Retrieve Update Delete

#List all the posts 

def base_view(request, *args, **kwargs):
    return render(request, "base.html", {})

def home_page_view(request,*args, **kwargs):
    print(request)
    print(request.user)
    return render(request, "home_page.html", {})

def contact_page_view(request, *args, **kwargs):

    return render(request, "contact_us.html", {})

def about_us_page_view(request,*args, **kwargs):
    return render(request, "about_us.html", {})

def signup_signin_page_view(request, *args, **kwargs):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(home_page_view)

    return render(request, "signin.html", {})

def signout_page_view(request):
    if request.method == "POST":
        logout(request)
        return render(request, "home_page.html", {})

def customer_signup_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.username = form.cleaned_data.get('username')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.save()
            #Save to db
            userName = request.POST.get('username')
            firstName = request.POST.get('first_name')
            lastName = request.POST.get('last_name')
            emailadd = request.POST.get('email')
            passwordc = request.POST.get('password1')
            passwordcon = request.POST.get('phone_number')

            customer = Customer.objects.create(
                user = user,
                username = userName,
                first_name= firstName, 
                last_name= lastName, 
                email= emailadd,
                password1= passwordc
                )
            customer.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(home_page_view)
        else: 
            print(form.errors)  
    else:
        form = CustomerSignUpForm()
    return render(request, "signup.html", {'form': form})

def business_signup_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = BusinessSignUpForm(request.POST)
        if form.is_valid():
            # user = form.save()
            # #Save to profiles
            # user.refresh_from_db()
            # user.profile.store_name = form.cleaned_data.get('store_name')
            # user.profile.store_number = form.cleaned_data.get('store_number')
            # user.profile.store_address = form.cleaned_data.get('store_address')
            # user.profile.city = form.cleaned_data.get('city')
            # user.profile.state = form.cleaned_data.get('state')
            # user.profile.zipcode = form.cleaned_data.get('zipcode')
            # user.profile.input_sex = form.cleaned_data.get('input_sex')
            # user.save()
            # #Save to db


            # raw_password = form.cleaned_data.get('password1')
            # # business = authenticate(username=user.username, password=raw_password)
            # login(request, business)
            return redirect(home_page_view)
        else: 
            print(form.errors)
    else:
        form = BusinessSignUpForm()
        return render(request, 'b_signup.html', {'form': form})
    return render(request, "b_signup.html", {})

def business_login_view(request, *args, **kwargs):
	return render(request, "b_login.html", {})

def forgot_password_view(request, *args, **kwargs):
	return render(request, "reset.html", {})

def control_panel_view(request, *args, **kwargs):
    return render(request, "control_panel.html", {})

def profile_setting_view(request, *args, **kwargs):
    return render(request, "profile_setting.html", {})
