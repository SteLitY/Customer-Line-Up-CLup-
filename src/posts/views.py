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
from .sms import enterqueue
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import *

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
        messages.success(request, "Successfuly Logged in for Line Up") 
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
                    return redirect ("/password_reset/done/")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

#Signs client out and redirects to homepage
def signout_page_view(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return render(request, "home_page.html", {}) 

#########################################################################################
#                                   Sign in views                                       #
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
@login_excluded('/')
def business_login_view(request, *args, **kwargs):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Successfuly Logged in for Line Up") 
                return redirect('/control_panel') 
    return render(request, "b_sigin.html", {})

#########################################################################################
#                                    Sign up views                                      #
#########################################################################################

#Customer sign up view
#Asks for username, name, email, number
#Username and password set is now their sigin information
#Redicts to 'line up' page where they can immediately get a ticket for a store 
@login_excluded('/')
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
            messages.success(request, "Successfully Signed Up for Line Up!")
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
@login_excluded('/')
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
            messages.success(request, 'Successfully Signed Up for Line Up!')
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
            messages.success(request, "Successfuly Logged in for Line Up") 
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
    # if ajax request
    # is_ajax() = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'. deprecated
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        print("IM TRYNA AJAX")
        if request.GET.get('change') == 'add':
            print('added')
            for item in obj:
                #If adding one more customer goes over store capacity, then dont adds
                if item.in_store+1 > item.store_capacity:
                    return HttpResponse("Store at max capacity")
                #If adding one more customer doesntgoes over store capacity, then add
                if item.in_store+1 <= item.store_capacity:
                    increase = item.in_store + 1
                    obj.update(in_store = increase)
            #Update database
            for item in obj:
                    item.save()
            print(increase)
            return HttpResponse (increase)
        elif request.GET.get('change') == 'remove':
            print('removed')
            for item in obj:
                #If removing one more customer goes under 0, then dont remove
                if item.in_store-1 == 0:
                    inside = 0
                    obj.update(in_store = 0)
                #If removing one more customer doesnt goes under 0, then remove
                if item.in_store-1 > 0:
                    inside = item.in_store - 1
                    obj.update(in_store = inside)
                #Update database
            for item in obj:
                    item.save()
            return HttpResponse (inside)
    else:
        #show page
        return render(request, "control_panel.html", {'obj':obj})


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
            messages.success(request, 'Successfully Updated Profile')
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
                messages.success(request, 'Successfully Updated Password')
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
            messages.success(request, 'Successfully Updated Profile')
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
                messages.success(request, 'Successfully Updated Password')
        cus = Customer.objects.all().filter(username = request.user.get_username())
    return render(request, "profile_setting.html", { 'cus': cus, 'bus': bus})

#########################################################################################
#                                    Ticketing views                                    #
#########################################################################################

#Displays store information: address, number and hours
#Allows client to search for store and filters out the list
#Allows client to enter/leave a line for a specific businesss
@user_must_login(please_login_view)
def line_up_view(request,*args, **kwargs):
    #search filter
    business = Business.objects.all().order_by('store_name')
    myFilter = business_search_filter(request.GET, queryset=business)
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

#store details view
@user_must_login(please_login_view)
def store_details_view(request):
    restaurant_name = request.GET.get('restName') #gets the store name
    current_business = Business.objects.filter(store_name=restaurant_name)[:1]
    restaurant = current_business.values()[0]
    res_num = restaurant["store_number"]

    #reusable variables by David
    store_group_limit = Business.objects.filter(store_name=restaurant_name)[0].group_limit #gets the store's group_limit
    current_user = request.user.get_username() #gets the currently logged in user
    #bool to check if user is already in the customer_queue for the current business
    is_user_in_queue = Customer_queue.objects.filter(store_name=restaurant_name, name = current_user).exists() 
    #formatted_phone_number = res_num[:3] + '-' + res_num[3:6] + '-' + res_num[6:]


    if request.method == 'POST':
        closed = request.POST.get("closed", None)
        form = CustomerLineUpForm(request.POST)
        #context needs to be updated in two places
        context = {**restaurant, "store_name":restaurant_name, "restaurant_number": res_num, "store_group_limit": store_group_limit,"form": form}

        #input for the forms
        group = request.POST.get('group_size')
        #if closed in ["smsuser"]:         #function from sms.py for texting when they enter queue
            #enterqueue(request.user.profile.phone_number, restaurant_name)

#this part checks for stupid user inputs
        #checks group_size for stupid inputs like: abc@#. /?
        if (group.isdigit() == False):
            messages.error(request, "Please enter a valid number.")
            # new_link = "store_details.html\?restName=" + str(restaurant_name)
            return render(request, "store_details.html", context)
        
        #checks to see if group_size is less than 1
        if (int(group)) <= 0:
            messages.error(request, "Your group size is too small.")
            # new_link = "store_details.html\?restName=" + str(restaurant_name)
            return render(request, "store_details.html", context)

        #checks to see if user is already in the queue for this business
        if is_user_in_queue == True:
            messages.error(request, "You are already on line for this store.")
            # new_link = "store_details.html\?restName=" + str(restaurant_name)
            return render(request, "store_details.html", context)
        
        #checks to see if business has group limit set up
        if (store_group_limit == '') or (int(store_group_limit) == 0):
            messages.error(request, "Business is temporarily not accepting more customers.")
            # new_link = "store_details.html\?restName=" + str(restaurant_name)
            return render(request, "store_details.html", context)
        

        #checks to see if group_size > group limit set by the store
        if (int(group)) > int(store_group_limit):
            messages.error(request, "Your group size exceeds the limit.")
            # new_link = "store_details.html\?restName=" + str(restaurant_name)
            return render(request, "store_details.html", context)

#this part is for position
        #check if another user is already in queue. If it is, then take the highest position in that store and add 1, if not, then position = 1.
        if Customer_queue.objects.filter(store_name=restaurant_name).exists():
            user_position = Customer_queue.objects.filter(store_name=restaurant_name).order_by('-position')[0].position + 1
        else:
            user_position = 1        
        
    #to do: (written by: David)
#   send email confirmation with links to exit line.
#   check if there's space in store:
#   if sum_of_group_size_on_queue_for_this_business + current_user's group_size < group_capacity: 
#       redirect to print QR code page and be sure to include webpage for "I'm near the vicinity"

        EnterInMySQL = Customer_queue.objects.create(
            name = current_user,
            position = user_position, 
            group_size = int(group),
            store_name = restaurant["store_name"],
            )
        EnterInMySQL.save()

        #after entering the user in queue, we update the business' model with the group_size
        bus = Business.objects.filter(store_name=restaurant_name)
        for item in bus:
            item.scheduled = item.scheduled + int(group)
            item.save()

        return redirect(customer_schedule_view)
    else: 
        form = CustomerLineUpForm()

        #context needs to be updated in two places
        context = {**restaurant, "store_name":restaurant_name, "restaurant_number": res_num, "store_group_limit": store_group_limit,"form": form}
    return render(request, "store_details.html", context)


#Page to leave the queue
@user_must_login(please_login_view)
def leave_line_view(request, *args, **kwargs):
    #reusable variables
    current_user = request.user.get_username() #gets the currently logged in user
    store = request.GET.get('store') #gets the store name
    user_in_store = Customer_queue.objects.filter(store_name=store, name=current_user)
    business = Business.objects.filter(store_name=store)
    
    if user_in_store.exists():
        head_count = Customer_queue.objects.filter(store_name=store, name=current_user)[0].group_size
    else:
        head_count = 0
        
    context = {'storeName':store, 'groupSize':head_count}
    if request.method == 'POST':
        form = CustomerLineUpForm(request.POST)
        if user_in_store.exists():
            delete_from_queue = Customer_queue.objects.filter(store_name=store, name=current_user)
            delete_from_queue.delete()

            for store in business:
                store.scheduled = store.scheduled - head_count
                store.save()
            
            messages.success(request, "You've left the line for " + str(store)) 
            return redirect("/customer_schedule/")
            #   to do: (Written By: David)
#   each time a user checks out:
#      check if users are on the queue (if sum_of_clients > group_limit). 
#      if there are user(s) on the queue and not "in the vicinity of the store", 
#           send email/text notifications to people who are next on line (ex: 5th online, 10th online, or 15th online, etc)
        else:
            messages.error(request, "You are not in line for " + str(store))

    return render(request, "leave_line.html", context)

#Shows the people who is registered for that business
def my_business_scheduled_view(request,*args, **kwargs):
    current_user = request.user.get_username()
    current_business_name = Business.objects.filter(username=current_user)[0].store_name
    scheduled = Customer_queue.objects.filter(store_name=current_business_name)

    context = {'scheduled':scheduled, 'current_business_name':current_business_name}
    return render(request, "my_business_scheduled.html", context)


#Shows the customer which business they're registered for
def customer_schedule_view(request,*args, **kwargs):
    #query variables to be passed to django template
    current_user = request.user.get_username()
    scheduled = Customer_queue.objects.filter(name=current_user)
    business = Business.objects.filter(store_name__isnull=False)

    #checking to see if user signed up for a store
    isEmpty = current_user
    if not scheduled:
        isEmpty = "You are not Scheduled for anything."

    context = {'business':business, 'scheduled':scheduled, 'current_user':current_user, 'isEmpty':isEmpty}
    return render(request, "customer_schedule.html", context)
