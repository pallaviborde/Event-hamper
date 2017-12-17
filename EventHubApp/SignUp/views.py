from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from EventHubApp.search.models import Category
from EventHubApp.registration.models import States
from django.shortcuts import render_to_response
from django.template import RequestContext


# @login_required
def home(request):
    list1 = Category.objects.all()
    stateNames = States.objects.order_by().values('city_state').distinct()
    cityNames = States.objects.order_by().values('city_name').distinct()
    #print("request.session: ", request.session)
    return render(request, 'home.html', {'list1' : list1, 'stateNames': stateNames, 'cityNames':cityNames})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            request.session["userid"] = 1
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    list1 = Category.objects.all()
    return render(request, 'signup.html', {'list1' : list1})
# Create your views here.
def getData(request):
    list1 = Category.objects.all()
    stateNames = States.objects.order_by().values('city_state').distinct()
    print('---list1',list1)
#     for i in list1:
#         print('----',i.testid)
    request.session["userid"] = 1
    return render(request, 'home.html', {'list1' : list1})

def test(request):
    list1 = Category.objects.all()
    print('---list1',list1)
#     for i in list1:
#         print('----',i.testid)
    request.session["userid"] = 1
    return render(request, 'test.html', {'list1' : list1})



# def selectview(request):
#     item  = Test.objects.all() # use filter() when you have sth to filter ;)
#     form = request.POST # you seem to misinterpret the use of form from django and POST data. you should take a look at [Django with forms][1]
#     # you can remove the preview assignment (form =request.POST)
#     if request.method == 'POST':
#         selected_item = get_object_or_404(Item, pk=request.POST.get('item_id'))
#         # get the user you want (connect for example) in the var "user"
#         user.item = selected_item
#         user.save()
#  
#       # Then, do a redirect for example
#  
#     return render_to_response ('select/item.html', {'items':item}, context_instance =  RequestContext(request),)

