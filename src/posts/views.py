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

from .models import *
from .forms import CustomerSignUpForm, BusinessSignUpForm
from .filters import business_search_filter
from django.views.generic import TemplateView

#requires user to login before they are allowed to go a page - David
def user_must_login(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if (request.user.is_authenticated == False):
                return redirect(redirect_to) 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

#requires user to be logged OUT to go to that page
def login_excluded(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to) 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

#########################################################################################


def please_login_view(request,*args, **kwargs):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(home_page_view) 
    return render(request, "please_login.html", {})


def base_view(request, *args, **kwargs):
    return render(request, "base.html", {})


def home_page_view(request,*args, **kwargs):
    return render(request, "home_page.html", {})


def contact_page_view(request, *args, **kwargs):
    return render(request, "contact_us.html", {})


def about_us_page_view(request,*args, **kwargs):
    return render(request, "about_us.html", {})


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

@user_must_login(home_page_view)
def signout_page_view(request):
    if request.method == "POST":
        logout(request)
        return render(request, "home_page.html", {})


@login_excluded(home_page_view)
def forgot_password_view(request, *args, **kwargs):
	return render(request, "reset.html", {})


@user_must_login(please_login_view)
def control_panel_view(request, *args, **kwargs):
    if request.user.profile.is_customer == True:
        return redirect(home_page_view)
    obj=Business.objects.all().filter(username = request.user.get_username())
    return render(request, "control_panel.html", {'obj':obj})


@user_must_login(please_login_view)
def profile_setting_view(request, *args, **kwargs):
    bus=Business.objects.all().filter(username = request.user.get_username())
    cus = Customer.objects.all().filter(username = request.user.get_username())
    #For Business
    if request.user.profile.is_business == True :
        if request.method == 'POST':
            closed = request.POST.get("closed", None)
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
            if closed in ["sclosed"]:
                bus.update(sunday_open = "00:00"),
                bus.update(sunday_closed = "00:00"),
            else:
                bus.update(sunday_open = request.POST.get('sunday_open')),
                bus.update(sunday_closed = request.POST.get('sunday_closed')),
            if closed in ["mclosed"]:
                bus.update(monday_open = "00:00"),
                bus.update(monday_closed = "00:00"),
            else: 
                bus.update(monday_open = request.POST.get('monday_open')),
                bus.update(monday_closed = request.POST.get('monday_closed')),
            if closed in ["tclosed"]:
                bus.update(tuesday_open = "00:00"),
                bus.update(tuesday_closed = "00:00"),
            else:
                bus.update(tuesday_open = request.POST.get('tuesday_open')),
                bus.update(tuesday_closed = request.POST.get('tuesday_closed')),
            if closed in ["wclosed"]:
                bus.update(wednesday_open = "00:00"),
                bus.update(wednesday_closed = "00:00"),
            else:
                bus.update(wednesday_open = request.POST.get('wednesday_open')),
                bus.update(wednesday_closed = request.POST.get('wednesday_closed')),
            if closed in ["thclosed"]:
                bus.update(thursday_open = "00:00"),
                bus.update(thursday_closed = "00:00"),
            else:
                bus.update(thursday_open = request.POST.get('thursday_open')),
                bus.update(thursday_closed = request.POST.get('thursday_closed')),
            if closed in ["fclosed"]:
                bus.update(friday_open = "00:00"),
                bus.update(friday_closed = "00:00"),
            else:
                bus.update(friday_open = request.POST.get('friday_open')),
                bus.update(friday_closed = request.POST.get('friday_closed')),
            if closed in ["saclosed"]:
                bus.update(saturday_open = "00:00"),
                bus.update(saturday_closed = "00:00"),
            else:
                bus.update(saturday_open = request.POST.get('saturday_open')),
                bus.update(saturday_closed = request.POST.get('saturday_closed')),
            bus.update(group_limit = request.POST.get('group_limit')),
            bus.update(store_capacity = request.POST.get('store_capacity'))
            for item in bus:
                item.save()
            password = request.POST.get("password2", None)
            if password is not None:
                username = request.user.get_username()
                password = request.POST['password1']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    new = User.objects.get(username= request.user.get_username())
                    new.set_password(request.POST.get('password2'))
                    new.save()
        bus=Business.objects.all().filter(username = request.user.get_username())
    #For customer
    if request.user.profile.is_customer == True :
        if request.method == 'POST':
            cus.update(first_name = request.POST.get('first_name')),
            cus.update(last_name = request.POST.get('last_name')),
            cus.update(email = request.POST.get('email')),
            cus.update(phone_number = request.POST.get('phone_number')),
            for item in cus:
                item.save()
            password = request.POST.get("password4", None)
            if password is not None:
                username = request.user.get_username()
                password = request.POST['password3']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    new = User.objects.get(username= request.user.get_username())
                    new.set_password(request.POST.get('password2'))
                    new.save()
        return render(request, "profile_setting.html", { 'cus': cus, 'bus': bus})
    return render(request, "profile_setting.html", { 'cus': cus, 'bus': bus})


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

@login_excluded('/line_up')
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
            return redirect('\line_up') 
        else: 
            print(form.errors)  
    else:
        form = CustomerSignUpForm()
    return render(request, "signup.html", {'form': form})

@login_excluded(control_panel_view)
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
            return redirect(home_page_view)
        else: 
            print(form.errors)
    else:
        form = BusinessSignUpForm()
        return render(request, 'b_signup.html', {'form': form})
    return render(request, "b_signup.html", {})


@login_excluded(control_panel_view)
def business_login_view(request, *args, **kwargs):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/control_panel') 
    return render(request, "b_login.html", {})
    
def customer_control_view(request, *args, **kwargs):
    return render(request, "customer_control.html", {})

def customer_profile_view(request, *args, **kwargs):
    return render(request, "customer_profile.html", {})

def scheduled_view(request, *args, **kwargs):
    return render(request, "scheduled.html", {})

@user_must_login(control_panel_view)
def line_up_view(request,*args, **kwargs):
    business = Business.objects.all()
    # myFilter = OrderFilter()
    return render(request, "lineup.html", {'business':business})

class HomeView(TemplateView):
    template_name = "home2.html"