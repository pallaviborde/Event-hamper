from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from EventHubApp.search.models import Category
from EventHubApp.search.models import UserProfile
from EventHubApp.search.models import Rating
from EventHubApp.search.models import User
from EventHubApp.search.models import Rating
from EventHubApp.registration.models import Userprofiledetails
from cart.cart import Cart
from django.template.context_processors import request
from EventHubApp.registration.models import States
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.core.serializers import serialize
import json

def getprofile(request):
    category_id = request.GET['category_id']
    request.session["categoryid"] = category_id
    print('catagory', category_id)
    category = Category.objects.get(category_id=category_id)
#     profiles = UserProfile.objects.filter(category_id = category_id )
    print('category',category)
    print('profiles',profiles)
    profiles = UserProfile.objects.filter(category_id=category_id, active=True)

    profileJsons=serialize('json', list(profiles))
    profileJsons = json.dumps(profileJsons)

    # print('category', category)
    # print('profiles', profiles)
    return render(request, 'listservice.html', {'profiles' : profiles, 'category' : category, 'profileJsons':profileJsons})


def getallprofile(request):
    searchText = request.POST.get('searchText')
    print('searchText', searchText)
    categoryids = Category.objects.values_list('category_id', flat=True).filter(
        Q(category_name__contains=searchText) | Q(description__contains=searchText))
    #     filter(category_name__contains=searchText)
    #     .filter(description__contains=searchText)
    print('categoryids', list(categoryids))
    profiles = UserProfile.objects.filter(active=True).filter(
        Q(profile_name__contains=searchText) | Q(description__contains=searchText) | Q(category_id__in=categoryids))
    #     filter(profile_name__contains=searchText).filter(description__contains=searchText).filter(category_id__in=categoryids)
    print('profiles', profiles)
    category = {
        'category_name': 'Services'
    }
    profileJsons = serialize('json', list(profiles))
    profileJsons = json.dumps(profileJsons)
    return render(request, 'listservice.html', {'profiles' : profiles, 'category' : category})



def getdetail(request):
    profile_id = request.GET['profile_id']
    print('profile_id', profile_id)
    #     category = Category.objects.get(category_id = category_id)
    profile = UserProfile.objects.get(profile_id=profile_id)
    profile_detail = Userprofiledetails.objects.get(profile_id=profile_id)
    print('profile_detail',profile_detail.type)
    print('profile',profile)
    range1 = range(1,6)
    feedback = Rating.objects.filter(profile = profile_id)
    print('profile_detail', profile_detail.type)
    print('profile', profile)
    # range1 = range(1,6)
    range1 = (profile.pic1, profile.pic2, profile.pic3, profile.pic4, profile.pic5)
    return render(request, 'viewdetail.html', {'range' : range1 , 'profile' : profile, 'profileDetails':profile_detail,'feedbacks':feedback })


def add_to_cart(request, product_id, quantity=1):
#     if "userid" in request.session:
#         userid = request.session["userid"]
    product = UserProfile.objects.get(profile_id=product_id)
    cart = Cart(request)
    cart.add(product, product.price, quantity)
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': dict(cart=Cart(request)), 'cartlength': cart.count(), 'tot': cart.summary() })


def remove_from_cart(request, product_id):
    product = UserProfile.objects.get(profile_id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return render(request, 'cart.html', {'cart': dict(cart=Cart(request)),'cartlength': cart.count(), 'tot': cart.summary() })


def get_cart(request):

    print('here')
    cart = Cart(request)
    return render(request,'cart.html', {'cart': dict(cart=Cart(request)), 'cartlength': cart.count(), 'tot': cart.summary() })


def getprofileonprice(request):
    if "categoryid" in request.session:
        category_id = request.session["categoryid"]
    category = Category.objects.get(category_id=category_id)
    if 'max' in request.GET and 'min' in request.GET:
        print('In GET')
        max_price = request.GET['max']
        min_price = request.GET['min']
    else: 
        max_price = request.POST['maxPrice']
        min_price = request.POST['minPrice']
        print('In POST')
    profiles = UserProfile.objects.filter(category_id = category_id ).filter(price__range=(min_price, max_price))
    
    return render(request, 'listservice.html', {'profiles' : profiles, 'category' : category})


def getprofileonrating(request):

    if "categoryid" in request.session:
        category_id = request.session["categoryid"]
    category = Category.objects.get(category_id = category_id)
    min_rating= request.GET['min_rating']
    max_rating= request.GET['max_rating']
    profile_ids=Rating.objects.values_list('profile_id', flat=True).filter(rating__range=(min_rating, max_rating))
    profiles = UserProfile.objects.filter(category_id = category_id ).filter(profile_id__in=profile_ids)
    return render(request, 'listservice.html', {'profiles' : profiles, 'category' : category})

def getprofileonstate(request):
    if "categoryid" in request.session:
        category_id = request.session["categoryid"]
    category = Category.objects.get(category_id = category_id)
    state = request.POST['stateName']
    user_id = User.objects.values_list('user_id', flat=True).filter(state=state)
    profiles = UserProfile.objects.filter(category_id = category_id ).filter(user_id__in=user_id)
    return render(request, 'listservice.html', {'profiles' : profiles, 'category' : category })

def getprofileonicity(request):
    if "categoryid" in request.session:
        category_id = request.session["categoryid"]
    category = Category.objects.get(category_id = category_id)
    city = request.POST['cityName']
    user_id = User.objects.values_list('user_id', flat=True).filter(city=city)
    profiles = UserProfile.objects.filter(category_id = category_id ).filter(user_id__in=user_id)
    return render(request, 'listservice.html', {'profiles' : profiles, 'category' : category })
# def getprofileonname(request):

def saverating(request, product_id):
    if "userid" in request.session:
        userid = request.session["userid"]
    feedback = request.POST.get('feedback')
    rating = request.POST.get('rating')
    print(rating)
    ratingprofile =  Rating(profile = UserProfile.objects.get(profile_id=product_id), rating = rating , description = feedback , user = User.objects.get(user_id = userid) )
    ratingprofile.save()

    return render(request, 'rating.html', {'profile_id' : product_id})

    

def redirectrating(request, product_id):
    return render(request, 'rating.html', {'profile_id' : product_id})


