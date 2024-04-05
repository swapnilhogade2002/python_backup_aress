from django.shortcuts import render,redirect
from django.views import View
from .models import Movies,OrderPlaced,Cart,Customer,TheaterTicketBooking
from .forms import CustomerRegistrationForms, CustomerProfileForm,LoginForm,Movies,MoviesForm
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import string
import random
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.template import RequestContext
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from django.template.loader import render_to_string
from io import BytesIO
from reportlab.pdfgen import canvas
from django.db.models import Value
from django.db.models.functions import Concat
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
# def home(request):
#  return render(request, 'app/home.html')

# class MoviesView(View):
#   def get(self,request):
#     entertaintment=Movies.objects.filter(category='E')
#     thriller=Movies.objects.filter(category='T')
#     romance=Movies.objects.filter(category='R')
#     science=Movies.objects.filter(category='SF')
#     return render(request,'app/home.html',
#     {'entertaintment':entertaintment,'thriller':thriller,'romance':romance,
#      'science':science})

class MoviesView(View):
    def get(self, request):
        query = request.GET.get('q')
        entertaintment = Movies.objects.filter(category='E')
        thriller = Movies.objects.filter(category='T')
        romance = Movies.objects.filter(category='R')
        science = Movies.objects.filter(category='SF')

        # Handle search functionality
        if query:
            entertaintment = entertaintment.filter(title__icontains=query)
            thriller = thriller.filter(title__icontains=query)
            romance = romance.filter(title__icontains=query)
            science = science.filter(title__icontains=query)

        return render(request, 'app/home.html', {
            'entertaintment': entertaintment,
            'thriller': thriller,
            'romance': romance,
            'science': science
        })

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
        if cart_item.quantity <= 0:
            cart_item.delete()  # Remove the movie from the cart if its quantity becomes zero or negative
        else:
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


def generate_ticket_pdf(request, order_id):
    order = OrderPlaced.objects.get(id=order_id)
    template_path = 'app/ticket_pdf_template.html'
    context = {'order': order}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{order_id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    p = canvas.Canvas(response)
    # Set the font and font size
    p.setFont("Helvetica", 12)

    # Write the ticket details
    p.drawString(100, 800, "Ticket Details:")
    p.drawString(100, 780, f"Movie Title: {order.product.titlee}")
    p.drawString(100, 760, f"Tickets: {order.quantity}")
    p.drawString(100, 740, f"Price Total Price: {order.product.discounted_price}")
    p.drawString(100, 720, f"Order date: {order.ordered_date}")
    p.drawString(100, 700, f"Theater: {order.product.theater_name}")
    p.drawString(100, 680, f"Address: {order.product.address}")
    p.drawString(100, 660, f"Show Time: {order.product.show_time}")
    p.drawString(100, 640, f"Booking Date&Time: {order.ordered_date}")

    # Determine the status and write it accordingly
    status_text = ''
    if order.status == 'Pending':
        status_text = 'Booking Pending'
    elif order.status == 'Booked':
        status_text = 'Ticket Booked'
    else:
        status_text = order.status
    p.drawString(100, 620, f"Status: {status_text}")


    p.showPage()
    p.save()

    return response

@login_required
def save_selected_seats(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        selected_seats = request.POST.getlist('selected-seats')

        # Assuming you have retrieved the current user
        user = request.user

        # Create a new instance of TheaterTicketBooking and save it
        booking = TheaterTicketBooking.objects.create(
            user=user,
            movie_id=product_id,
            seats=", ".join(selected_seats)  # Convert the list of seats to a string
        )
        booking.save()

        # Redirect or render a success page
        return redirect('checkout')  # Replace 'success_page' with the URL name of your success page
    else:
        # Retrieve the selected seats data from the database for the current user and movie
        product_id = request.POST.get('product_id')
        user = request.user
        selected_seats = TheaterTicketBooking.objects.filter(user=user, movie_id=product_id).values_list('seats', flat=True)

        # Retrieve booked seats for the specific movie
        booked_seats = TheaterTicketBooking.objects.values_list('seats', flat=True)
        print(booked_seats)

        # Generate the range of available seat numbers
        seat_range = range(1, 11)  # Assuming there are 10 seats

        # Pass the selected seats, booked seats, and seat range data to the template context
        return render(request, 'cart', {'selected_seats': selected_seats, 'booked_seats': booked_seats, 'seat_range': seat_range})

    
def change_password(request):
 return render(request, 'app/changepassword.html')

# def mobile(request):
#  return render(request, 'app/mobile.html')

# def thriller_sort(request, data=None):
#     if data is None:
#         thriller_movies = Movies.objects.filter(category='T')
#     else:
#         if data == 'name_asc':
#             thriller_movies = Movies.objects.filter(category='T').order_by('titlee')
#             print(thriller_movies)
#         elif data == 'name_desc':
#             thriller_movies = Movies.objects.filter(category='T').order_by('-titlee')
#             print(thriller_movies)
#     return render(request, 'app/movie_sort.html', {'thriller_movies': thriller_movies})

def thriller_sort(request, data=None):
    query = request.GET.get('q')
    
    if query:
        # Filter movies based on title or theater name if search query is provided
        thriller_movies = Movies.objects.filter(category='T').filter(
            Q(titlee__icontains=query) | Q(theater_name__icontains=query)
        )
    else:
        # Otherwise, apply sorting if 'data' parameter is provided
        if data is None:
            thriller_movies = Movies.objects.filter(category='T')
        else:
            if data == 'name_asc':
                thriller_movies = Movies.objects.filter(category='T').order_by('titlee')
            elif data == 'name_desc':
                thriller_movies = Movies.objects.filter(category='T').order_by('-titlee')
    
    # Pagination
    paginator = Paginator(thriller_movies, 1)  # Show 3 movies per page
    page_number = request.GET.get('page')
    try:
        thriller_movies = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        thriller_movies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        thriller_movies = paginator.page(paginator.num_pages)
    
    return render(request, 'app/movie_sort.html', {'thriller_movies': thriller_movies})

def entertaintment_sort(request, data=None):
    query = request.GET.get('q')
    
    if query:
        # Filter movies based on title or theater name if search query is provided
        entertaintment_movies = Movies.objects.filter(category='E').filter(
            Q(titlee__icontains=query) | Q(theater_name__icontains=query)
        )
    else:
        if data is None:
            entertaintment_movies = Movies.objects.filter(category='E')
        else:
            if data == 'name_asc':
                entertaintment_movies = Movies.objects.filter(category='E').order_by('titlee')
            elif data == 'name_desc':
                entertaintment_movies = Movies.objects.filter(category='E').order_by('-titlee')
    
    # Pagination
    paginator = Paginator(entertaintment_movies, 1)  # Show 3 movies per page
    page_number = request.GET.get('page')
    try:
        entertaintment_movies = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        entertaintment_movies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        entertaintment_movies = paginator.page(paginator.num_pages)
    return render(request, 'app/entertain_sort.html', {'entertaintment_movies': entertaintment_movies})

def romantic_sort(request, data=None):
    query = request.GET.get('q')
    
    if query:
        # Filter movies based on title or theater name if search query is provided
        romantic_movies = Movies.objects.filter(category='R').filter(
            Q(titlee__icontains=query) | Q(theater_name__icontains=query)
        )
    else:
        if data is None:
            romantic_movies = Movies.objects.filter(category='R')
        else:
            if data == 'name_asc':
                romantic_movies = Movies.objects.filter(category='R').order_by('titlee')
            elif data == 'name_desc':
                romantic_movies = Movies.objects.filter(category='R').order_by('-titlee')
    
    # Pagination
    paginator = Paginator(romantic_movies, 1)  # Show 3 movies per page
    page_number = request.GET.get('page')
    try:
        romantic_movies = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        romantic_movies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        romantic_movies = paginator.page(paginator.num_pages)
    
    return render(request, 'app/romantic_sort.html', {'romantic_movies': romantic_movies})

# def login(request):
#  return render(request, 'app/login.html')


def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    return otp
 
# def custom_login(request):
#     if not request.user.is_authenticated:
#         if request.method == 'POST':
#             fa = LoginForm(request=request, data=request.POST)
#             if fa.is_valid():
#                 uname = fa.cleaned_data['username']
#                 upass = fa.cleaned_data['password']
#                 user = authenticate(username=uname, password=upass)
#                 if user is not None:
#                     # Generate OTP
#                     otp = generate_otp()
#                     # You can do something with this OTP, such as send it via SMS or email
#                     print("Generated OTP:", otp)
#                     # Store the OTP in the user session for validation later
#                     request.session['otp'] = otp
#                     request.session['username'] = uname  # Store username for OTP validation
#                     request.session['password']=upass
                   
#                     # Redirect to OTP verification page
#                     return redirect('verify_otp')
#         else:
#             fa = LoginForm()
#         return render(request, 'app/login.html', {'form': fa})
#     else:
#         return redirect('profile')

def custom_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fa = LoginForm(request=request, data=request.POST)
            if fa.is_valid():
                uname = fa.cleaned_data['username']
                upass = fa.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    # Generate OTP
                    otp = generate_otp()
                    # You can do something with this OTP, such as send it via SMS or email
                    print("Generated OTP:", otp)
                    # Store the OTP in the user session for validation later
                    request.session['otp'] = otp
                    request.session['username'] = uname  # Store username for OTP validation
                    request.session['password'] = upass

                    # Redirect to OTP verification page
                    return redirect('verify_otp')
        else:
            fa = LoginForm()
        return render(request, 'app/login.html', {'form': fa})
    else:
        return redirect('profile')


 
# def verify_otp(request):
#     if request.method == 'POST':
#         entered_otp = request.POST.get('otp')
#         stored_otp = request.session.get('otp')
       
#         print("Entered OTP:", entered_otp)
#         print("Stored OTP:", stored_otp)
       
#         if entered_otp == stored_otp:
#             # OTP matched, proceed with login
#             uname = request.session.get('username')
#             upass = request.session.get('password')
#             print(uname)
#             print(upass)
#             user = authenticate(username=uname, password=upass)
#             print("Authenticated User:", user)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "Successfully logged in!")
#                 return redirect('profile')
#             else:
#                 messages.error(request, "Authentication failed. User not found.")
#                 print("Authentication failed. User not found.")
#         else:
#             messages.error(request, "Invalid OTP. Please try again.")
#             print("OTP verification failed.")
#     return render(request, 'app/verify_otp.html')


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if entered_otp == stored_otp:
            uname = request.session.get('username')
            upass = request.session.get('password')
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in!")
                if user.groups.filter(name='Theater').exists():
                    # If user belongs to 'Theater' group, render theater_dashboard.html
                    return redirect ('moviesviewtheater')
                else:
                    # If user does not belong to 'Theater' group, redirect to profile page
                    return redirect('profile')
            else:
                messages.error(request, "Authentication failed. User not found.")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'app/verify_otp.html')

# testing dashboard 
# def verify_otp(request):
#     if request.method == 'GET':
#         uname = request.session.get('username')
#         upass = request.session.get('password')
#         user = authenticate(username=uname, password=upass)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Successfully logged in!")
#             if user.groups.filter(name='Theater').exists():
#                 # If user belongs to 'Theater' group, render theater_dashboard.html
#                 return render(request, 'theater/theater_dashboard.html')
#             else:
#                 # If user does not belong to 'Theater' group, redirect to profile page
#                 return redirect('profile')
#         else:
#             messages.error(request, "Authentication failed. User not found.")

#     return render(request, 'app/verify_otp.html')


# login to different dashboard

# class CustomLoginView(LoginView):
#     template_name = 'app/login.html'  # Specify your custom login template

#     def form_valid(self, form):
#         # Get the authenticated user
#         user = form.get_user()
        
#         # Check if the user belongs to the 'Theater' group
#         if user.groups.filter(name='Theater').exists():
#             # Redirect to theater dashboard if the user belongs to the 'Theater' group
#             messages.info(self.request, 'Welcome to the Theater Dashboard!')
#             return redirect('theater_dashboard')  # Adjust the URL name as per your URL configuration
#         else:
#             # Redirect to normal dashboard for users not belonging to the 'Theater' group
#             messages.info(self.request, 'Welcome to the user Dashboard!')
#             return redirect('normal_dashboard')  # Adjust the URL name as per your URL configuration
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.user
#         return context

# def custom_login(request):
#     return render(request, 'app/login.html', context_instance=RequestContext(request))


# def theater_dashboard(request):
#     return render(request, 'app/theater_dashboard.html')



# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

# class CustomerRegistrationView(View):
#   def get(self,request):
#     form=CustomerRegistrationForms()
#     return render(request, 'app/customerregistration.html',{'form':form})
  
#   def post(self,request):
#     form = CustomerRegistrationForms(request.POST)
#     if form.is_valid():
#       messages.success(request,'Congratulations ! Succesfully Registered .')
#       form.save()
#     return render(request, 'app/customerregistration.html',{'form':form})
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForms()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForms(request.POST)
        if form.is_valid():
            roll = form.cleaned_data.get('roll')
            if roll == 'theater':
                # Assign user to the "Theater" group
                theater_group = Group.objects.get(name='Theater')
                user = form.save()
                theater_group.user_set.add(user)

                messages.success(request, 'Congratulations! Successfully Registered.')
                return redirect('login') 
            else:
                messages.success(request, 'Congratulations! Successfully Registered.')
                form.save()
                return redirect('login')

        return render(request, 'app/login.html', {'form': form})  

def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    CGST_rate = 8 / 100  # CGST rate of 8%
    SGST_rate = 5 / 100  # SGST rate of 5%
    total_amount = 0.0
    CGST_total = 0.0
    SGST_total = 0.0
    
    booked_seats = []  # Initialize list to store booked seats

    for item in cart_items:
        temp_amount = item.quantity * item.product.discounted_price
        CGST = temp_amount * CGST_rate  # Calculating CGST for the item
        SGST = temp_amount * SGST_rate  # Calculating SGST for the item
        total_amount += temp_amount + CGST + SGST  # Accumulating total amount for all items
        CGST_total += CGST
        SGST_total += SGST

        total_amount += temp_amount + CGST + SGST
 

    return render(request, 'app/checkout.html', {'total_amount': total_amount,'cart_items':cart_items})


def book_tickets(request):
    if request.method == 'POST':
        selected_seats = request.POST.getlist('selected_seats')
        user = request.user  # Assuming user is authenticated
        movie_id = request.POST.get('movie_id')  # Assuming you pass movie_id in your form

        # Concatenate selected seats into a single string
        seats_string = ",".join(selected_seats)

        # Create a TheaterTicketBooking object with concatenated seats
        booking = TheaterTicketBooking(user=user, movie_id=movie_id, seat=seats_string)
        booking.save()

        return redirect('checkout')  # Redirect to booking success page or any other page

    return render(request, 'checkout.html')

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

# theater dashboard
@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MoviesForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user  # Set the added_by field to the current user
            movie.save()
            return redirect('addmovie')  # Redirect to a success page
    else:
        form = MoviesForm()
    return render(request, 'theater/add_movie.html', {'form': form})

class MoviesViewTheater(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user  # Get the logged-in user
        query = request.GET.get('q')
        
        # Filter movies based on the logged-in user
        movies = Movies.objects.filter(added_by=user)
        print(movies)

        # Handle search functionality
        if query:
            movies = movies.filter(title__icontains=query)

        return render(request, 'theater/show_movie.html', {'movies': movies})
    
class EditMovieView(UpdateView):
    model = Movies
    fields = ['titlee', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image', 'theater_name', 'show_time', 'address']
    template_name = 'theater/edit_movie.html'
    success_url = reverse_lazy('moviesviewtheater')

class DeleteMovieView(DeleteView):
    model = Movies
    template_name = 'theater/delete_movie.html'
    success_url = reverse_lazy('moviesviewtheater')