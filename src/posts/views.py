from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
# Create your views here.

#CRUD Create Retrieve Update Delete

#List all the posts 

def home_page_view(request,*args, **kwargs):
    print(request)
    print(request.user)
    return render(request, "homepage.html", {})


def contact_page_view(request, *args, **kwargs):
    return render(request, "contact.html", {})

def about_us_page_view(request,*args, **kwargs):
     return render(request, "aboutus.html", {})

