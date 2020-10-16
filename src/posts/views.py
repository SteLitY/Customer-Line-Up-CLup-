from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
from django.shortcuts import render, redirect
from .models import Post
from .forms import CustomerSignUpForm
from .forms import BusinessSignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string


# from mysite.core.forms import SignUpForm

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

def about_us_page_view(request,*args, **kwargs):
    return render(request, "about_us.html", {})

def signup_signin_page_view(request, *args, **kwargs):
    return render(request, "signin.html", {})

def customer_signup_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.cell_number = form.cleaned_data.get('cell_number')
            user.save()
            user.refresh_from_db()
            # user_username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return render(request, "home_page.html", {})
            # return redirect(home_page_view)
        else: 
            print("here")
            print(form.errors)  
    else:
        form = CustomerSignUpForm()
    return render(request, "signup.html", {'form': form})

def business_signup_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = BusinessSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.Business1.store_name = form.cleaned_data.get('store_name')
            user.Business1.store_number = form.cleaned_data.get('store_number')
            user.Business1.store_address = form.cleaned_data.get('store_address')
            user.Business1.city = form.cleaned_data.get('city')
            user.Business1.state = form.cleaned_data.get('state')
            user.Business1.zipcode = form.cleaned_data.get('zipcode')
            user.Business1.input_sex = form.cleaned_data.get('input_sex')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(home_page_view)
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

