from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.shortcuts import render_to_response
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
import importlib.util
import sys
import os
from .models import *
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
# Import Folder model
# from filer.models.foldermodels import Folder
from EventHubApp.search.models import User, UserProfile, Category
from EventHubApp.events.models import User
from django.contrib.auth.models import User as DUser
from django.contrib.auth import authenticate
from EventHubApp.registration.models import States, Userprofiledetails
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
import random
from django.contrib import messages



# Displays contact.html
def contact(request):
    template = loader.get_template('contact.html')
    context = {

    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'contact.html')


# Display aboutUs.html
def aboutUs(request):
    template = loader.get_template('aboutUs.html')
    context = {

    }
    return render(request, 'aboutUs.html')


# save Contact Us Form
def contactUs(request):
    contactInstance = Contact()

    # userDetails = User.objects.get(username='Amruta')
    contactInstance.userid = 1
    contactInstance.email = request.POST.get('emailId')
    contactInstance.reason = request.POST.get('reason')
    contactInstance.messsage = request.POST.get('message')
    contactInstance.save()
    return render(request, 'contactConfirmation.html')


def signin(request):
    name = request.GET['username']
    pwd = request.GET['password']
    # message = 'You entered username : %r' % name
    # message = 'You entered password : %r' % pwd
    # return HttpResponse(message)
    #result = User.objects.filter(username=name).exists()
    #return HttpResponse(result)
    try:
        duser = authenticate(username=name, password=pwd)
        print(duser)
        user = User.objects.get(username=name, password = pwd)
    except User.DoesNotExist:
        return render(request,'nologinsuccess.html')
    else:
        request.session["userid"] = user.user_id
        #template = loader.get_template('home.html')
        return render(request, 'home.html')

    # result = User.objects.filter(username=name).exists()
    # return HttpResponse(result)
    user = User.objects.get(username=name, password=pwd);
    if user:
        request.session["userid"] = user.user_id
        request.session["username"] = user.username
        template = loader.get_template('home.html')
        return render(request, 'home.html')
    else:
        return render(request, 'nologinsuccess.html')


def signup(request):
    template = loader.get_template('signup.html')
    context = {
    }
    return render(request, 'signup.html')


def signupSubmit(request):
    try:
        firstname = request.POST.get('inputFname')
        lastname = request.POST.get('inputLname')
        email = request.POST.get('emailId')
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')
        street1 = request.POST.get('street1')
        street2 = request.POST.get('street2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin_number = request.POST.get('pin_number')
        phone = request.POST.get('phone')

        # hashed = b.hashpw(passwd, b.gensalt())

        userProfile = User(first_name=firstname, last_name=lastname, email=email, username=username,
                           password=passwd, street1=street1, street2=street2, city=city, state=state,
                           country=country, phone=phone)
        userProfile.user_type_id_id = 1
        userProfile.verifyFlag = False
        userProfile.save()
        uid = userProfile.user_id
        message = sendVerifyLink(email,uid)
        messages.success(request, message)
        return render(request, 'signup.html')
    except:
        messages.warning(request, 'Oops! Something went wrong. Please fill form again')
        return render(request, 'signup.html')
    
def forgotPass(request):
#     template = loader.get_template('evforgotPass.html')
#     context = {
#     }
    return render(request, 'forgotPass.html')

def sendEmail(request):
    email = request.GET['emailId']
    forgotPass(request)
    if User.objects.filter(email = email).exists():
        sub = "Event Hub: Password Reset request"
        s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        passlen = 8
        p = "".join(random.sample(s, passlen))
        content = "Hello, \n\nYou requested for new password for your Event Hub account." \
                  "\nPlease find below your password:\n" \
                  "\nYour password: %s" % p + "\n" + "\nIf it is not you please change password for security." \
                                            "\n\nRegards, " \
                                              "\n\nEvent Hub Team"
        send_mail(sub, content, 'event.hub.team@gmail.com', [email], fail_silently=False)
        messages.success(request, 'Your password was sent to your email-Id successfully!')
        User.objects.filter(email = email).update(password = p)
        return render(request, 'forgotPass.html')
    else:
        # message = "Please enter correct email id."
        messages.warning(request, 'Please enter correct email id.')
        return render(request,'forgotPass.html')

def sendVerifyLink(email, uid):
    #code here for verification email send. This function will be called in signupsubmit
    if User.objects.filter(email=email).exists():
        sub = "Event Hub: Verify your email id"
        link = "http://127.0.0.1:8000/activate_email/%s" % uid
        content = "Hello, \n\nVerify your Event Hub account." \
                  "\nClick on following link:\n\n %s" %link + "\n" + "\n\nRegards," \
                                                                     "Event Hub Team"

        send_mail(sub, content, 'event.hub.team@gmail.com', [email], fail_silently=False)

        message = "We have sent you a verification link to your email. Please verify your account!"
        return message
    else:
        message = 'Failed to send email for verification...'
        return message

def activate_email(request,uid):
    try:
        User.objects.filter(user_id = uid).update(verifyFlag = True)
        messages.success(request, 'Your account is activated successfully!')
        return render(request, "home.html")
    except:
        messages.warning(request, 'Please verify your email id.')
        return render(request, "home.html")

