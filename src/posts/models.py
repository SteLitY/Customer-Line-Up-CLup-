from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django import forms 

class Post(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField() 

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=31, blank=True)
    cell_number = models.CharField(max_length=12, blank=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#Customer Registration
class Customer(models.Model):
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    email =  models.CharField(max_length=127, default='123@aol.com')
    password = models.CharField(max_length=10, default='')

    def __unicode__(self):
        return u'%s %s %s %s' % (self.first_name, self.last_name, self.email, self.password)

#business table
class business(models.Model):
    email = models.CharField(max_length=127, default='')
    first_name = models.CharField(max_length=127, default='')
    middle_name = models.CharField(max_length=127, default='')
    last_name = models.CharField(max_length=127, default='')
    password = models.CharField(max_length=127, default='')
    cellnumber = models.CharField(max_length=127, default='')

    
#business table
class Business1(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, blank=True)
    store_name = models.CharField(max_length=100, blank=True)
    store_number = models.CharField(max_length=12, blank=True)
    store_address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=30, default='Ny')
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.CharField(max_length=5, blank=True)
    input_sex = models.CharField(max_length=3, null=True)


@receiver(post_save, sender=User)
def create_user_profile1(sender, instance, created, **kwargs):
    if created:
        Business1.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile1(sender, instance, **kwargs):
    instance.profile.save()

