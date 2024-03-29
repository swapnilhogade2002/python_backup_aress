from django.shortcuts import render,redirect
from django.views import View
from .models import Movies,OrderPlaced,Cart,Customer
from .forms import CustomerRegistrationForms, CustomerProfileForm
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.http import JsonResponse
# def home(request):
#  return render(request, 'app/home.html')

class MoviesView(View):
  def get(self,request):
    entertaintment=Movies.objects.filter(category='E')
    thriller=Movies.objects.filter(category='T')
    romance=Movies.objects.filter(category='R')
    science=Movies.objects.filter(category='SF')
    return render(request,'app/home.html',
    {'entertaintment':entertaintment,'thriller':thriller,'romance':romance,
     'science':science})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class MoviesDetailView(View):
  def get(self, request, pk):
    movie=Movies.objects.get(pk=pk)
    return render(request,'app/productdetail.html',{'movie':movie})

def add_to_cart(request):
  user=request.user
  movie_id=request.GET.get('movie_id')
  print(movie_id)
  movie=Movies.objects.get(id=movie_id)
  print(movie)
  reg=Cart(user=user,product=movie)
  reg.save()
  return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        if cart.exists():  # Check if cart is not empty
            print(cart)
            CGST_rate = 8 / 100  # CGST rate of 8%
            SGST_rate = 5 / 100  # SGST rate of 5%
            total_amount = 0.0
            CGST_total = 0.0
            SGST_total = 0.0
            for item in cart:
                temp_amount = item.quantity * item.product.discounted_price
                CGST = temp_amount * CGST_rate  # Calculating CGST for the item
                SGST = temp_amount * SGST_rate  # Calculating SGST for the item
                total_amount += temp_amount + CGST + SGST  # Accumulating total amount for all items
                CGST_total += CGST
                SGST_total += SGST
            print(cart)
            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': total_amount, 'CGST': CGST_total, 'SGST': SGST_total})
        else:
            return render(request,'app/emptycart.html')  # Redirect to another view if cart is empty
    else:
        return redirect('login_view')  # Redirect to login view if user is not authenticated
        

def plus_cart(request):
    if request.method == 'GET' and request.user.is_authenticated:
        movie_id = request.GET.get('movie_id')
        cart_item = Cart.objects.get(Q(product__id=movie_id) & Q(user=request.user))
        cart_item.quantity += 1
        cart_item.save()

        # Recalculate total amount, CGST, and SGST after updating the cart
        CGST_rate = 8 / 100  # CGST rate of 8%
        SGST_rate = 5 / 100  # SGST rate of 5%
        total_amount = 0.0
        CGST_total = 0.0
        SGST_total = 0.0

        cart = Cart.objects.filter(user=request.user)
        for item in cart:
            temp_amount = item.quantity * item.product.discounted_price
            CGST = temp_amount * CGST_rate  # Calculating CGST for the item
            SGST = temp_amount * SGST_rate  # Calculating SGST for the item
            total_amount += temp_amount + CGST + SGST  # Accumulating total amount for all items
            CGST_total += CGST
            SGST_total += SGST
            

        return JsonResponse({'total_amount': total_amount, 'CGST': CGST_total, 'SGST': SGST_total})
    else:
        return JsonResponse({'error': 'Invalid request or user not authenticated'})


def minus_cart(request):
    if request.method == 'GET' and request.user.is_authenticated:
        movie_id = request.GET.get('movie_id')
        cart_item = Cart.objects.get(Q(product__id=movie_id) & Q(user=request.user))
        cart_item.quantity -= 1
        cart_item.save()

        # Recalculate total amount, CGST, and SGST after updating the cart
        CGST_rate = 8 / 100  # CGST rate of 8%
        SGST_rate = 5 / 100  # SGST rate of 5%
        total_amount = 0.0
        CGST_total = 0.0
        SGST_total = 0.0

        cart = Cart.objects.filter(user=request.user)
        for item in cart:
            temp_amount = item.quantity * item.product.discounted_price
            CGST = temp_amount * CGST_rate  # Calculating CGST for the item
            SGST = temp_amount * SGST_rate  # Calculating SGST for the item
            total_amount += temp_amount + CGST + SGST  # Accumulating total amount for all items
            CGST_total += CGST
            SGST_total += SGST
            

        return JsonResponse({'total_amount': total_amount, 'CGST': CGST_total, 'SGST': SGST_total})
    else:
        return JsonResponse({'error': 'Invalid request or user not authenticated'})

def remove_cart(request):
    if request.method == 'GET' and request.user.is_authenticated:
        movie_id = request.GET.get('movie_id')
        print(movie_id)  # Use print() to log to console
        try:
            cart_item = Cart.objects.get(product__id=movie_id, user=request.user)
            cart_item.delete()

            # Recalculate total amount, CGST, and SGST after updating the cart
            CGST_rate = 8 / 100  # CGST rate of 8%
            SGST_rate = 5 / 100  # SGST rate of 5%
            total_amount = 0.0
            CGST_total = 0.0
            SGST_total = 0.0

            cart = Cart.objects.filter(user=request.user)
            for item in cart:
                temp_amount = item.quantity * item.product.discounted_price
                CGST = temp_amount * CGST_rate  # Calculating CGST for the item
                SGST = temp_amount * SGST_rate  # Calculating SGST for the item
                total_amount += temp_amount + CGST + SGST  # Accumulating total amount for all items
                CGST_total += CGST
                SGST_total += SGST

            return JsonResponse({'total_amount': total_amount, 'CGST': CGST_total, 'SGST': SGST_total})
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found for the given movie ID'})
    else:
        return JsonResponse({'error': 'Invalid request or user not authenticated'})
      
def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
    ticket_history=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'ticket_history':ticket_history})

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request):
 return render(request, 'app/mobile.html')

# def mobile(request , data=None):
#   if data==None:
#     romance=Movies.objects.filter(category='Romance')
#     return render(request, 'app/mobile.html',{'romance':romance})
#   elif data=''

def login(request):
 return render(request, 'app/login.html')



# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
  def get(self,request):
    form=CustomerRegistrationForms()
    return render(request, 'app/customerregistration.html',{'form':form})
  
  def post(self,request):
    form = CustomerRegistrationForms(request.POST)
    if form.is_valid():
      messages.success(request,'Congratulations ! Succesfully Registered .')
      form.save()
    return render(request, 'app/customerregistration.html',{'form':form})
    
    

def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    CGST_rate = 8 / 100  # CGST rate of 8%
    SGST_rate = 5 / 100  # SGST rate of 5%
    total_amount = 0.0
    CGST_total = 0.0
    SGST_total = 0.0

    for item in cart_items:
        temp_amount = item.quantity * item.product.discounted_price
        CGST = temp_amount * CGST_rate  # Calculating CGST for the item
        SGST = temp_amount * SGST_rate  # Calculating SGST for the item
        total_amount += temp_amount + CGST + SGST  # Accumulating total amount for all items
        CGST_total += CGST
        SGST_total += SGST

    total_amount += temp_amount + CGST + SGST

    return render(request, 'app/checkout.html', {'total_amount': total_amount,'cart_items':cart_items})

def payment_done(request):
    user=request.user
    custid=request.user.id
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")
    print(id)
    return render(request, 'app/payment_done.html')



class ProfileView(View):  
  def get(self, request):
        try:
            user_profile = Customer.objects.filter(user=request.user).first()
            if user_profile:
                form = CustomerProfileForm(instance=user_profile)
            else:
                form = CustomerProfileForm()
        except MultipleObjectsReturned:
            form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
  
  def post(self,request):
    form= CustomerProfileForm(request.POST)
    if form.is_valid():
      usr=request.user
      name=form.cleaned_data['name']
      locality=form.cleaned_data['locality']
      city=form.cleaned_data['city']
      state=form.cleaned_data['state']
      zipcode=form.cleaned_data['zipcode']
      reg=Customer(user=usr,name=name,locality=locality,city=city,state=state
                   ,zipcode=zipcode)
      reg.save()
      messages.success(request,'Congratulation !!! Profile Updated Successfully.')
    return render(request,'app/profile.html',{'form':form, 'active':'btn-primary'})

