from django.db import models
from django.forms import ModelForm
# from django.core.validators import RegexValidator
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField

# from EventHubApp.search.models import User, UserProfile


class Contact(models.Model):
    userid = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=50)
    reason = models.CharField(max_length=50)
    messsage = models.CharField(max_length=50)
    createdDate = models.DateTimeField(auto_now_add=True)
    lastUpdatedDate = models.DateTimeField(auto_now=True)

class User(models.Model):
    # user_id = models.IntegerField(primary_key=True)
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=60)
    street1 = models.CharField(max_length=50)
    street2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pin_number = models.IntegerField
    phone = PhoneNumberField(blank=True, null=True)
    verifyFlag = models.BooleanField(default=False)

    def __str__(self):  # __unicode__ on Python 2
        return self.username