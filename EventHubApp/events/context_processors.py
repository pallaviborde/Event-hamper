from EventHubApp.search.models import User
from cart.cart import Cart
from EventHubApp.search.models import Category
def add_username_to_context(request):
    states = User.objects.values_list('state', flat=True).distinct()
    cities = User.objects.values_list('city', flat=True).distinct()
    cart = Cart(request)
    list1 = Category.objects.all()
    if 'userid' in request.session:
        userid = request.session.get('userid')
        isLoggedIn = True;
    else:
        userid = 0
        isLoggedIn = False;
    return {
        'username': request.session.get('username'),
        'isLoggedIn': isLoggedIn,
        'states' : states,
        'cities' : cities,
        'list1' : list1, 
        'cartlength': cart.count(), 
        'tot': cart.summary()
    }