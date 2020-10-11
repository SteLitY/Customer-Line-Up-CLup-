from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
from django.shortcuts import render, redirect
from .models import Post
from .forms import CustomerSignUpForm
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

from posts.forms import CustomerSignUpForm

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
    return render(request, "aboutus.html", {})

def signup_signin_page_view(request, *args, **kwargs):
    return render(request, "signin.html", {})

def customer_signup_view(request, *args, **kwargs):

    return render(request, "signup.html", {})

    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.middle_name = form.cleaned_data.get('middle_name')
            user.profile.cell_number = form.cleaned_data.get('cell_number')
            user.save()
            user.refresh_from_db()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(home_page_view)
    else:
        form = CustomerSignUpForm()
    return render(request, "signup.html", {'form': form})
    # if request.method == 'POST':
    #     form = CustomerSignUpForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         user.refresh_from_db()  # load the profile instance created by the signal
    #         user.profile.middle_name = form.cleaned_data.get('middle_name')
    #         user.save()
    #         raw_password = form.cleaned_data.get('password1')
    #         user = authenticate(username=user.username, password=raw_password)
    #         login(request, user)
    #         return redirect('c_signup.html')
    #     else:
    #         form = CustomerSignUpForm()
    #     return render(request, 'c_signup.html', {'form': form})

def business_signup_view(request, *args, **kwargs):
    return render(request, "b_signup.html", {})

def business_login_view(request, *args, **kwargs):
	return render(request, "b_login.html", {})

def forgot_password_view(request, *args, **kwargs):
	return render(request, "reset.html", {})

def control_panel_view(request, *args, **kwargs):
    return render(request, "control_panel.html", {})

    
def control_panel_view(request, *args, **kwargs):
    return render(request, "control_panel.html", {})

def profile_setting_view(request, *args, **kwargs):
    return render(request, "profile_setting.html", {})

