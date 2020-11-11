from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Business)
admin.site.register(Profile) 
admin.site.register(Customer)
admin.site.register(All_Customers)


