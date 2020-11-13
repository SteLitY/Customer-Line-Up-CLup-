from django.http import HttpResponse
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
from django.core.mail import send_mail, BadHeaderError #password reset
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q #password reset
from django.contrib.auth.tokens import default_token_generator #password reset
from django.contrib import messages #import messages for passsword
from posts.forms import CustomerSignUpForm
from django.forms import inlineformset_factory
from .sms import sendtext

from .models import *
from .forms import CustomerSignUpForm, BusinessSignUpForm
from .filters import business_search_filter

#########################################################################################
#                                  Requirements                                         #
#########################################################################################

#Requires user to login before they are allowed to go a page - David
def user_must_login(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if (request.user.is_authenticated == False):
                return redirect(redirect_to) 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

#Requires user to be logged OUT to go to that page
#Redirects them to another page
def login_excluded(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to) 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

#########################################################################################
#                                  Exclusions                                           #
#########################################################################################

# If trying to access a page that you need to be logged on to see,
# redirects to 'Please login' view
@login_excluded('/') 
def please_login_view(request,*args, **kwargs):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/') 
    return render(request, "please_login.html", {})

#########################################################################################
#                                   Default views                                       #
#########################################################################################

# Displays the homepage
# If signed in, displays the username, and appropriate links in navbar
# else, displays 'Line Up', and non-personal links in navbar
def home_page_view(request,*args, **kwargs):
    return render(request, "home_page.html", {})

#Displays our github link
def contact_page_view(request, *args, **kwargs):
    return render(request, "contact_us.html", {})

#Displays our project mission 
def about_us_page_view(request,*args, **kwargs):
    return render(request, "about_us.html", {})

#########################################################################################
#                                Forgot password views and Sign OUT                     #
#########################################################################################

#This page allows clients to reset their password via email
#@login_excluded(home_page_view) #Doesnt stop anything
def forgot_password_view(request, *args, **kwargs):
    return render(request, "reset.html", {})
#This page allows clients to reset their password via email
#Checked email against database, if found, send them the link 
#Else displays invalid email
@login_excluded(home_page_view)
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Line Up',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'david.chen68@myhunter.cuny.edu', [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')
                        
                    messages.success(request, 'A message with the reset password instructions has been sent to your inbox.')
                    return redirect ("/password_reset/done/")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

#Signs client out and redirects to homepage
def signout_page_view(request):
    logout(request)
    return render(request, "home_page.html", {}) 

#########################################################################################
#                                   Sign in views              c                        #
#########################################################################################

#Customer sign in page
#Asks for username and password, checks against database
#if valid, login in the customer
@login_excluded('/line_up') 
def signup_signin_page_view(request, *args, **kwargs):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/line_up')
    return render(request, "signin.html", {})

#Business sign in page
#Asks for username and password, checks against database
#if valid, login in the business
def business_login_view(request, *args, **kwargs):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/control_panel') 
    return render(request, "b_sigin.html", {})

#########################################################################################
#                                    Sign up views                                      #
#########################################################################################

#Customer sign up view
#Asks for username, name, email, number
#Username and password set is now their sigin information
#Redicts to 'line up' page where they can immediately get a ticket for a store 
def customer_signup_view(request, *args, **kwargs):
    if request.method == 'POST' and request.POST['action'] == 'Customer':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # Create user profile
            user.profile.username = form.cleaned_data.get('username')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.is_customer = True
            user.save()
           #sendtext(user.profile.phone_number, user.profile.first_name)  #sends text to customer when they sign up
            #Save to db
            customer = Customer.objects.create(
                username = request.POST.get('username'),
                first_name= request.POST.get('first_name'), 
                last_name= request.POST.get('last_name'), 
                email= request.POST.get('email'),
                phone_number  = request.POST.get('phone_number')
                )
            raw_password = form.cleaned_data.get('password1')
            customer = authenticate(username=user.username, password=raw_password)
            login(request, customer)
            return redirect('/line_up') 
        else: 
            print(form.errors)  
    else:
        form = CustomerSignUpForm()
    return render(request, "signup.html", {'form': form})

#Business sign up view
#At sign up, only ask for basic infomation, for the page to not look over crowded
#Asks for username, name, email, number, store: name, address, number
#Username and password set is now their sigin information
#Once signed in, they're redirected to 'Profile Settings' where they can input 
#other information such as: Store hours, group limit, store capacity 
#and able to change password
def business_signup_view(request, *args, **kwargs):
    if request.method == 'POST'and request.POST['action'] == 'Business':
        form = BusinessSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            #Save to profiles
            user.refresh_from_db()
            user.profile.username = form.cleaned_data.get('username')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.is_business = True
            user.save()
            # #Save to db
            business = Business.objects.create(
                username = request.POST.get('username'),
                first_name = request.POST.get('first_name'),
                last_name= request.POST.get('last_name'), 
                email= request.POST.get('email'),
                phone_number = request.POST.get('phone_number'),
                store_name = request.POST.get('store_name'),
                store_number = request.POST.get('store_number'),
                store_address = request.POST.get('store_address'),
                city = request.POST.get('city'),
                state = request.POST.get('state'),
                zipcode = request.POST.get('zipcode'),
                )
            raw_password = form.cleaned_data.get('password1')
            business = authenticate(username=user.username, password=raw_password)
            login(request, business)
            return redirect(profile_setting_view)
        else: 
            print(form.errors)
    else:
        form = BusinessSignUpForm()
        return render(request, 'b_signup.html', {'form': form})
    return render(request, "b_signup.html", {})

#########################################################################################
#                                   Personalized views                                  #
#########################################################################################

#Control panel
#Able to see the number of customers in store, in line and schedule to arrive
#Can manually checkin and check out customers as well
@user_must_login(please_login_view)
def control_panel_view(request, *args, **kwargs):
    #redirect customers if they find themselves at this link 
    if request.user.profile.is_customer == True:
        return redirect(home_page_view)
    obj=Business.objects.all().filter(username = request.user.get_username())
    #Add customer to queue
    if request.method == 'POST' and request.POST['action'] == 'add':
        for item in obj:
            #If adding one more customer goes over store capacity, then dont add
            if item.in_store+1 > item.store_capacity:
                pass
            #If adding one more customer doesntgoes over store capacity, then add
            if item.in_store+1 <= item.store_capacity:
                inside = item.in_store + 1
                print(inside)
                obj.update(in_store = inside)
        #Update database
        for item in obj:
                item.save()
    #Remove customer from queue
    if request.method == 'POST' and request.POST['action'] == 'remove':
        for item in obj:
            #If removing one more customer goes under 0, then dont remove
            if item.in_store-1 == 0:
                obj.update(in_store = 0)
            #If removing one more customer doesnt goes under 0, then remove
            if item.in_store-1 > 0:
                inside = item.in_store - 1
                obj.update(in_store = inside)
        #Update database
        for item in obj:
                item.save()
    obj=Business.objects.all().filter(username = request.user.get_username())
    return render(request, "control_panel.html", {'obj':obj})

#Shows profile settings based on who is logged in
#If you are a customer displays:
#   username, email, name, number and option to change password
#If you are a business displays:
#   Personal: username, email, name, number and option to change password
#   Store: name, address, number, hours, group limit, group capacity
#For password change, it only changes password if there is information 
#entered in the 'new password' field. 
#Upon entering, it validates 'current password' against database,
#if it is valid, it changes, else it does nothing.
#Upon hitting save, all information is updated in database
@user_must_login(please_login_view)
def profile_setting_view(request, *args, **kwargs):
    #Get table for customer/business
    bus=Business.objects.all().filter(username = request.user.get_username())
    cus = Customer.objects.all().filter(username = request.user.get_username())
    #For Business
    if request.user.profile.is_business == True :
        if request.method == 'POST':
            closed = request.POST.get("closed", None)
            #Update every field except store hours
            bus.update(first_name = request.POST.get('first_name')),
            bus.update(last_name= request.POST.get('last_name')), 
            bus.update(email= request.POST.get('email')),
            bus.update(phone_number = request.POST.get('phone_number')),
            bus.update(store_name = request.POST.get('store_name')),
            bus.update(store_number = request.POST.get('store_number')),
            bus.update(store_address = request.POST.get('store_address')),
            bus.update(city = request.POST.get('city')),
            bus.update(state = request.POST.get('state')),
            bus.update(zipcode = request.POST.get('zipcode')),
            bus.update(group_limit = request.POST.get('group_limit')),
            bus.update(store_capacity = request.POST.get('store_capacity'))
            #If Sunday is checked closed, set values to closed
            if closed in ["sclosed"]:
                bus.update(sunday_open = "00:00"),
                bus.update(sunday_closed = "00:00"),
            #else set to choosen hours   
            else:
                bus.update(sunday_open = request.POST.get('sunday_open')),
                bus.update(sunday_closed = request.POST.get('sunday_closed')),
            #If Monday is checked closed, set values to closed
            if closed in ["mclosed"]:
                bus.update(monday_open = "00:00"),
                bus.update(monday_closed = "00:00"),
            #else set to choosen hours  
            else: 
                bus.update(monday_open = request.POST.get('monday_open')),
                bus.update(monday_closed = request.POST.get('monday_closed')),
            #If Tuesday is checked closed, set values to closed
            if closed in ["tclosed"]:
                bus.update(tuesday_open = "00:00"),
                bus.update(tuesday_closed = "00:00"),
            #else set to choosen hours  
            else:
                bus.update(tuesday_open = request.POST.get('tuesday_open')),
                bus.update(tuesday_closed = request.POST.get('tuesday_closed')),
            #If Wednesday is checked closed, set values to closed
            if closed in ["wclosed"]:
                bus.update(wednesday_open = "00:00"),
                bus.update(wednesday_closed = "00:00"),
            #else set to choosen hours  
            else:
                bus.update(wednesday_open = request.POST.get('wednesday_open')),
                bus.update(wednesday_closed = request.POST.get('wednesday_closed')),
            #If Thursday is checked closed, set values to closed
            if closed in ["thclosed"]:
                bus.update(thursday_open = "00:00"),
                bus.update(thursday_closed = "00:00"),
            #else set to choosen hours  
            else:
                bus.update(thursday_open = request.POST.get('thursday_open')),
                bus.update(thursday_closed = request.POST.get('thursday_closed')),
            #If Friday is checked closed, set values to closed
            if closed in ["fclosed"]:
                bus.update(friday_open = "00:00"),
                bus.update(friday_closed = "00:00"),
            #else set to choosen hours  
            else:
                bus.update(friday_open = request.POST.get('friday_open')),
                bus.update(friday_closed = request.POST.get('friday_closed')),
            #If Saturday is checked closed, set values to closed
            if closed in ["saclosed"]:
                bus.update(saturday_open = "00:00"),
                bus.update(saturday_closed = "00:00"),
            #else set to choosen hours  
            else:
                bus.update(saturday_open = request.POST.get('saturday_open')),
                bus.update(saturday_closed = request.POST.get('saturday_closed')),
            #Update database
            for item in bus:
                item.save()
            #If there is a value in password2 (meaning changing password)
            password = request.POST.get("password2", None)
            if password is not None:
                #Check entered 'current password' against password in database
                username = request.user.get_username()
                password = request.POST['password1']
                #If the passwords match
                user = authenticate(request, username=username, password=password)
                #Set password to the newly entered password
                if user is not None:
                    new = User.objects.get(username= request.user.get_username())
                    new.set_password(request.POST.get('password2'))
                    new.save()
        #Refresh database
    bus = Business.objects.all().filter(username = request.user.get_username())
    #For customer
    if request.user.profile.is_customer == True :
        if request.method == 'POST':
            #Update every field
            cus.update(first_name = request.POST.get('first_name')),
            cus.update(last_name = request.POST.get('last_name')),
            cus.update(email = request.POST.get('email')),
            cus.update(phone_number = request.POST.get('phone_number')),
            #Update database
            for item in cus:
                item.save()
            #If there is a value in password4 (meaning changing password)
            password = request.POST.get("password4", None)
            if password is not None:
                #Check entered 'current password' against password in database
                username = request.user.get_username()
                password = request.POST['password3']
                #If the passwords match
                user = authenticate(request, username=username, password=password)
                #Set password to the newly entered password
                if user is not None:
                    new = User.objects.get(username= request.user.get_username())
                    new.set_password(request.POST.get('password2'))
                    new.save()
        cus = Customer.objects.all().filter(username = request.user.get_username())
    return render(request, "profile_setting.html", { 'cus': cus, 'bus': bus})

#########################################################################################
#                                    Ticketing views                                    #
#########################################################################################

#Displays store information: address, number and hours
#Allows client to search for  store and filters out the list
#Allows client to enter/leave a line for a specific businesss
#Displays client's place in line, if the entered line
@user_must_login(please_login_view)
def line_up_view(request,*args, **kwargs):
    business = Business.objects.all().order_by('store_name')
    myFilter = business_search_filter(request.GET ,queryset=business)
    business = myFilter.qs
    return render(request, "lineup.html", {'business':business, 'myFilter':myFilter})

#Allows customer to schedule a time slot for a ticket
@user_must_login(please_login_view)
def customer_control_view(request, *args, **kwargs):
    return render(request, "customer_control.html", {})

#Notifies customer that they have been scheduled
@user_must_login(please_login_view)
def scheduled_view(request, *args, **kwargs):
    return render(request, "scheduled.html", {})
