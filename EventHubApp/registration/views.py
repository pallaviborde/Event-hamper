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
from EventHubApp.search.models import User, UserProfile, Category
from django.contrib import messages


categoryName = Category.objects.order_by("category_name")


# Displays registerServiceDetails.html
def registerServiceDetails(request):
    list1 = Category.objects.all()
    #stateNames = States.objects.order_by().values('city_state').distinct()
    #cityNames = States.objects.order_by().values('city_name').distinct()
    if 'userid' in request.session:
        userid = request.session.get('userid')
    else:
        userid = 0
        return render(request, 'home.html', {'list1': list1, 'loginRequired': True})
    userCategories = Category.objects.exclude(
        category_id__in=UserProfile.objects.filter(user_id=userid).values_list('category_id', flat=True))
    template = loader.get_template('registerServiceDetails.html')
    context = {

    }
    return render(request, 'registerServiceDetails.html', {'userCategories': userCategories})



# Create your views here.
def saveCategory(newCat):
    categoryInstance = Category()
    categoryInstance.category_name = newCat
    categoryInstance.description = newCat
    categoryInstance.category_url = newCat
    categoryInstance.save()


def saveUserProfile(request):
    list1 = Category.objects.all()
    #stateNames = States.objects.order_by().values('city_state').distinct()
    #cityNames = States.objects.order_by().values('city_name').distinct()

    if 'userid' in request.session:
        userid = request.session.get('userid')
    else:
        userid = 0
    categoryFlag = 0
    profileDetails = UserProfile()
    serviceCategory = request.POST.get('category')

    if serviceCategory == 'Other':
        newCat = request.POST.get('newCategory')
        saveCategory(newCat)

        categoryInfo = Category.objects.get(category_name=newCat)
        profileDetails.category_id = categoryInfo.category_id
        profileDetails.description = newCat
    else:
        categoryFlag = 1
        categoryDetails = Category.objects.get(category_name=serviceCategory)
        profileDetails.category_id = categoryDetails.category_id
        profileDetails.description = categoryDetails.category_name

    profileDetails.profile_name = request.POST.get('profileName')
    # userDetails = User.objects.all()
#     userDetails = User.objects.get(username='Amruta')
    profileDetails.user_id = userid

    # if not os.path.exists("EventHubApp/static/events/assets/img/media/" + "Test"):
    # os.makedirs("EventHubApp/static/events/assets/img/media/" + "Test")

    fs = FileSystemStorage()

    pic1 = request.FILES.get('pic1')
    pic2 = request.FILES.get('pic2')
    pic3 = request.FILES.get('pic3')
    pic4 = request.FILES.get('pic4')
    pic5 = request.FILES.get('pic5')

    if pic1:
        userPic1 = request.FILES['pic1']
        fs.save(userPic1.name, userPic1)
        profileDetails.pic1 = userPic1.name
    if pic2:
        userPic2 = request.FILES['pic2']
        fs.save(userPic2.name, userPic2)
        profileDetails.pic2 = userPic2.name
    if pic3:
        userPic3 = request.FILES['pic3']
        fs.save(userPic3.name, userPic3)
        profileDetails.pic3 = userPic3.name
    if pic4:
        userPic4 = request.FILES['pic4']
        fs.save(userPic4.name, userPic4)
        profileDetails.pic4 = userPic4.name
    if pic5:
        userPic5 = request.FILES['pic5']
        fs.save(userPic5.name, userPic5)
        profileDetails.pic5 = userPic5.name

    profileDetails.price = float(request.POST.get('sprice'))

    profileDetails.save()

    SPDetails = Userprofiledetails()

    if categoryFlag == 1:
        categoryDetails = Category.objects.get(category_name=serviceCategory)
    else:
        categoryDetails = Category.objects.get(category_name=request.POST.get('newCategory'))

    SPDetails.profile = UserProfile.objects.get(user_id=userid, category_id=categoryDetails.category_id)
    SPDetails.serviceName = request.POST.get('sname')
    SPDetails.type = request.POST.get('stype')
    SPDetails.offers = request.POST.get('soffer')
    SPDetails.package = request.POST.get('spackage')
    SPDetails.servicedetails = request.POST.get('sdetails')
    SPDetails.productdescription = request.POST.get('sdesc')
    SPDetails.aboutproduct = request.POST.get('sprod')
    SPDetails.aboutus = request.POST.get('sabout')
    SPDetails.save()

    return render(request, 'home.html')


def account(request):
    list1 = Category.objects.all()
    #stateNames = States.objects.order_by().values('city_state').distinct()
    #cityNames = States.objects.order_by().values('city_name').distinct()

    if 'userid' in request.session:
        userid = request.session.get('userid')
        username = request.session.get('username')
        print(username)
        print("userid: ", userid)
    else:
        userid = 0
        return render(request, 'home.html', {'list1': list1, 'loginRequired': True})

    userDetails = User.objects.get(user_id=userid)
    profileDetails = UserProfile.objects.filter(user_id=userid)

    if not profileDetails:
        template = loader.get_template('regularUserAccount.html')
        context = {

        }
        return render(request, 'regularUserAccount.html',
                      {
                       'userDetails': userDetails})
    else:
        userCategories = Category.objects.filter(
            category_id__in=UserProfile.objects.filter(user_id=userid).values_list('category_id', flat=True))
        DisabledProfiles = UserProfile.objects.filter(user_id=userid, active=False)
        template = loader.get_template('serviceUserAccount.html')
        context = {

        }
        return render(request, 'serviceUserAccount.html',
                      {'profileDetails': profileDetails,
                       'userDetails': userDetails,'userCategories': userCategories,'DisabledProfiles': DisabledProfiles})


def modifyServiceUserProfile(request):
    list1 = Category.objects.all()
    #stateNames = States.objects.order_by().values('city_state').distinct()
    #cityNames = States.objects.order_by().values('city_name').distinct()

    if 'userid' in request.session:
        userid = request.session.get('userid')
    else:
        userid = 0
        return render(request, 'home.html', {'list1': list1, 'loginRequired': True})

    userInstance = User.objects.get(user_id=userid)

    if request.POST.get('phone'):
        userInstance.phone = request.POST.get('phone')
    if request.POST.get('street1'):
        userInstance.street1 = request.POST.get('street1')
    if request.POST.get('street2'):
        userInstance.street2 = request.POST.get('street2')
    if request.POST.get('cityName'):
        userInstance.city = request.POST.get('cityName')
    if request.POST.get('stateName'):
        userInstance.state = request.POST.get('stateName')
    if request.POST.get('pin'):
        userInstance.pin_number = request.POST.get('pin')

    userInstance.save()

    # Disable Profile
    if request.POST.get('disableProfile'):
        disableProfile = request.POST.get('disableProfile')
        print(disableProfile)
        disableProfileInstance = UserProfile.objects.get(profile_id=disableProfile)
        disableProfileInstance.active = False
        disableProfileInstance.save()

    # Enable Profile
    if request.POST.get('enableProfile'):
        disableProfile = request.POST.get('enableProfile')
        enableProfileInstance = UserProfile.objects.get(profile_id=disableProfile)
        enableProfileInstance.active = True
        enableProfileInstance.save()

    categoryID = request.POST.get('categoryID')

    if categoryID:
        profileData = UserProfile.objects.get(user_id=userid, category_id=categoryID)
        profileDetailsData = Userprofiledetails.objects.get(profile_id=profileData.profile_id)
        return render(request, 'serviceProfileUpdate.html',
                      {'profileData': profileData,
                       'profileDetailsData': profileDetailsData})
    else:
        return render(request, 'home.html')


def updateUserProfileDetails(request):
    profileID = request.POST.get('pid')
    # print("profile_id:" , profileID)
    list1 = Category.objects.all()
    #stateNames = States.objects.order_by().values('city_state').distinct()
    #cityNames = States.objects.order_by().values('city_name').distinct()

    if 'userid' in request.session:
        userid = request.session.get('userid')
    else:
        userid = 0
        return render(request, 'home.html', {'list1': list1, 'loginRequired': True})

    profileDetailsInstance = Userprofiledetails.objects.get(profile_id=profileID)
    profileInstance = UserProfile.objects.get(profile_id=profileID)

    if request.POST.get('stype'):
        profileDetailsInstance.type = request.POST.get('stype')
    if request.POST.get('soffer'):
        profileDetailsInstance.offers = request.POST.get('soffer')
    if request.POST.get('spackage'):
        profileDetailsInstance.package = request.POST.get('spackage')
    if request.POST.get('sdetails'):
        profileDetailsInstance.servicedetails = request.POST.get('sdetails')
    if request.POST.get('sdesc'):
        profileDetailsInstance.productdescription = request.POST.get('sdesc')
    if request.POST.get('sprod'):
        profileDetailsInstance.aboutproduct = request.POST.get('sprod')
    if request.POST.get('sabout'):
        profileDetailsInstance.aboutus = request.POST.get('sabout')

    profileDetailsInstance.save()

    if request.POST.get('price'):
        profileInstance.price = request.POST.get('price')


    fs = FileSystemStorage()

    pic1 = request.FILES.get('pic1')
    pic2 = request.FILES.get('pic2')
    pic3 = request.FILES.get('pic3')
    pic4 = request.FILES.get('pic4')
    pic5 = request.FILES.get('pic5')

    if pic1:
        userPic1 = request.FILES['pic1']
        fs.save(userPic1.name, userPic1)
        profileInstance.pic1 = userPic1.name
    if pic2:
        userPic2 = request.FILES['pic2']
        fs.save(userPic2.name, userPic2)
        profileInstance.pic2 = userPic2.name
    if pic3:
        userPic3 = request.FILES['pic3']
        fs.save(userPic3.name, userPic3)
        profileInstance.pic3 = userPic3.name
    if pic4:
        userPic4 = request.FILES['pic4']
        fs.save(userPic4.name, userPic4)
        profileInstance.pic4 = userPic4.name
    if pic5:
        userPic5 = request.FILES['pic5']
        fs.save(userPic5.name, userPic5)
        profileInstance.pic5 = userPic5.name

    profileInstance.save()

    return render(request, 'home.html')


def modifyRegularUserProfile(request):
    list1 = Category.objects.all()
    #stateNames = States.objects.order_by().values('city_state').distinct()
    #cityNames = States.objects.order_by().values('city_name').distinct()

    if 'userid' in request.session:
        userid = request.session.get('userid')
    else:
        userid = 0
        return render(request, 'home.html', {'list1': list1, 'loginRequired': True})

    userInstance = User.objects.get(user_id=userid)

    if request.POST.get('phone'):
        userInstance.phone = request.POST.get('phone')
    if request.POST.get('street1'):
        userInstance.street1 = request.POST.get('street1')
    if request.POST.get('street2'):
        userInstance.street2 = request.POST.get('street2')
    if request.POST.get('cityName'):
        userInstance.city = request.POST.get('cityName')
    if request.POST.get('stateName'):
        userInstance.state = request.POST.get('stateName')
    if request.POST.get('pin'):
        userInstance.pin_number = request.POST.get('pin')

    userInstance.save()
    return render(request, 'home.html')