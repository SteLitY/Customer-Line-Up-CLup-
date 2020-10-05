from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
# Create your views here.

#CRUD Create Retrieve Update Delete

#List all the posts 


def base_view(request, *args, **kwargs):
    return render(request, "base.html", {})

def home_page_view(request,*args, **kwargs):
    print(request)
    print(request.user)
    return render(request, "homepage.html", {})

def contact_page_view(request, *args, **kwargs):
    return render(request, "contact.html", {})

def about_us_page_view(request,*args, **kwargs):
     return render(request, "aboutus.html", {})

def signup_signin_page_view(request, *args, **kwargs):
    return render(request, "c_signin.html", {})

def customer_signup_view(request, *args, **kwargs):
    return render(request, "c_signup.html", {})

def business_signup_view(request, *args, **kwargs):
    return render(request, "b_signup.html", {})

def business_login_view(request, *args, **kwargs):
	return render(request, "b_login.html", {})

def forgot_password_view(request, *args, **kwargs):
	return render(request, "reset.html", {})
def control_panel_view(request, *args, **kwargs):
    return render(request, "controlpanel.html", {})
