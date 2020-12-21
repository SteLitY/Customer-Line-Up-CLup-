# CustomerLineup 
Authors: Ethan Sam, Kasey Harvey, David Chen, Mengzhen Zhao Christos Kamaris
Link to deployment: http://64.225.27.198:8000/

The goal of this project is to develop an easy-to-use webapp that:
1. Allows stores to regulate the amount of people inside the store

2. Save the client’s time from having to physically wait in line (especially when the
weather is bad). 
3. Make sure the store continues to remains profitable with our line management system. Attention will also be given to the store’s profits (ex: the more people in the store, the more money the store earns. So, we need to let clients in as soon as there is space
available). If we don’t pay attention to the store’s profit, they will not use the app. 

Staff and managerial personnel will be able to see the amount of people within their store and
the amount of people in the queue. A QR code is generated for those who sign up on
the web application. Individuals or groups will scan their QR codes to get into the store,
when they are finished shopping, a cashier will scan them out, and the next person or
group may enter the store.


### Dependencies
1. Donwload Python 3.8 
<https://www.python.org/downloads/>

3. Install mySQL
* This will allow you to manage data migrations\
```pip install mysqlclient```
* If you encounter any errors with this, [click here](https://stackoverflow.com/questions/35190465/virtualenvpython3-4-pip-install-mysqlclient-error)

4. Install other libraries
* ```pip install django-crispy-forms``` This will allow forgot password forms to work

* ```pip install django-ses``` This is for sending emails for things like "forgot password". 

* ```pip install django-filter``` This is a search filter

* ```pip install qrcode``` This is to generate the qrcode
* ```pip install pillow``` Supports qrcode
* ```pip install dj_Static ``` 

## How to use:

1. open cmd (windows) or terminal and navigate to the src folder using the cd command

2. type: "python manage.py runserver"

3. open http://127.0.0.1:8000/

## Functions I've written (doesn't include the ones that I've contributed on).

#### In views.py:
def user_must_login(redirect_to)

def login_excluded(redirect_to)

def please_login_view(request,*args, **kwargs)

def password_reset_request(request)

def line_up_view(request,*args, **kwargs)

def leave_line_view(request, *args, **kwargs)

def my_business_scheduled_view(request,*args, **kwargs)

def remove_scheduled_view(request,*args, **kwargs)

