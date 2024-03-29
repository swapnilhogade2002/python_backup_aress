from django.shortcuts import render,redirect
from django.views import View
from .models import Movies,OrderPlaced,Cart,Customer
from .forms import CustomerRegistrationForms, CustomerProfileForm
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView

class MoviesView(View):
    """
    View class to handle rendering of the home page with categorized movies.

    Attributes:
        None

    Methods:
        get(self, request): Renders the home page with categorized movies.
    """

    def get(self, request):
        """
        Handle GET request to render the home page with categorized movies.

        Args:
            request: HttpRequest object containing metadata about the request.

        Returns:
            HttpResponse object: Rendered home page with categorized movies.

        Raises:
            None
        """
        # Query movies based on categories
        entertaintment = Movies.objects.filter(category='E')
        thriller = Movies.objects.filter(category='T')
        romance = Movies.objects.filter(category='R')
        science = Movies.objects.filter(category='SF')

        # Render the home page with categorized movies
        return render(request, 'app/home.html', {
            'entertaintment': entertaintment,
            'thriller': thriller,
            'romance': romance,
            'science': science
        })

# Movie detail view with login required decorator
@method_decorator(login_required, name='dispatch')
class MoviesDetailView(View):
    """
    View class to display details of a movie.

    Attributes:
        None

    Methods:
        get(self, request, pk): Handles GET request to display movie details.
    """

    def get(self, request, pk):
        """
        Handle GET request to display movie details.

        Args:
            request: HttpRequest object containing metadata about the request.
            pk (int): Primary key of the movie to display details.

        Returns:
            HttpResponse object: Rendered movie detail page.

        Raises:
            Movies.DoesNotExist: If the movie with the specified primary key does not exist.
        """
        # Retrieve movie details from the database
        try:
            movie = Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            # Handle case where movie does not exist
            return render(request, 'app/error.html', {'error_message': 'Movie does not exist'})

        # Render movie detail page with movie details
        return render(request, 'app/productdetail.html', {'movie': movie})


# Add to cart view with login required decorator
@login_required
def add_to_cart(request):
    """
    Add movie to cart.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse object: Redirect to cart page after adding movie to cart.
    """
    # Retrieve user and movie ID from the request
    user = request.user
    movie_id = request.GET.get('movie_id')

    # Retrieve movie object from the database
    try:
        movie = Movies.objects.get(id=movie_id)
    except Movies.DoesNotExist:
        # Handle case where movie does not exist
        return render(request, 'app/error.html', {'error_message': 'Movie does not exist'})

    # Create cart item and save it to the database
    cart_item = Cart(user=user, product=movie)
    cart_item.save()

    # Redirect to cart page
    return redirect('/cart')


# Show cart view with login required decorator
@login_required
def show_cart(request):
    """
    Display user's cart.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse object: Rendered cart page with cart items.
    """
    # Retrieve user's cart items
    user = request.user
    cart = Cart.objects.filter(user=user)

    # Check if cart is empty
    if cart.exists():
        # Calculate total amount, CGST, and SGST
        total_amount = 0.0
        CGST_total = 0.0
        SGST_total = 0.0
        CGST_rate = 8 / 100  # CGST rate of 8%
        SGST_rate = 5 / 100  # SGST rate of 5%
        for item in cart:
            temp_amount = item.quantity * item.product.discounted_price
            CGST = temp_amount * CGST_rate
            SGST = temp_amount * SGST_rate
            total_amount += temp_amount + CGST + SGST
            CGST_total += CGST
            SGST_total += SGST

        # Round total amount, CGST, and SGST to two decimal places
        total_amount = round(total_amount, 2)
        CGST_total = round(CGST_total, 2)
        SGST_total = round(SGST_total, 2)

        # Render cart page with cart items and total amounts
        return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': total_amount, 'CGST': CGST_total, 'SGST': SGST_total})
    else:
        # Render empty cart page if cart is empty
        return render(request, 'app/emptycart.html')

@login_required
def plus_cart(request):
    """
    Increase the quantity of a movie in the cart.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        JsonResponse: JSON response containing the updated total amount, CGST, and SGST.

    """
    if request.method == 'GET':
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

        # Round the total amount, CGST, and SGST to two decimal places
        total_amount = round(total_amount, 2)
        CGST_total = round(CGST_total, 2)
        SGST_total = round(SGST_total, 2)

        return JsonResponse({'total_amount': total_amount, 'CGST': CGST_total, 'SGST': SGST_total})
    else:
        return JsonResponse({'error': 'Invalid request or user not authenticated'})


@login_required
def minus_cart(request):
    """
    Decrease the quantity of a movie in the cart.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        JsonResponse: JSON response containing the updated total amount, CGST, and SGST.

    """
    if request.method == 'GET':
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

        # Round the total amount, CGST, and SGST to two decimal places
        total_amount = round(total_amount, 2)
        CGST_total = round(CGST_total, 2)
        SGST_total = round(SGST_total, 2)

        return JsonResponse({'total_amount': total_amount, 'CGST': CGST_total, 'SGST': SGST_total})
    else:
        return JsonResponse({'error': 'Invalid request or user not authenticated'})

@login_required
def remove_cart(request):
    """
    Remove a movie from the cart.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        JsonResponse: JSON response containing the updated amount and total amount.
    """
    if request.method == 'GET':
        movie_id = request.GET['movie_id']
        c = Cart.objects.get(Q(product__id=movie_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 50
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
        for p in cart_product:
            tempamount = (p.quantity * float(p.product.discounted_price))
            amount +=tempamount
            total_amount = amount+shipping_amount
            data ={
                'amount':amount,
                'total_amount' : total_amount 
            }
        return JsonResponse(data)
    
# View for rendering the buy now page
def buy_now(request):
    return render(request, 'app/buynow.html')

# View for rendering the profile page
def profile(request):
    return render(request, 'app/profile.html')

# View for rendering the address page
def address(request):
    return render(request, 'app/address.html')

# View for rendering the orders page and fetching order history of the user
def orders(request):
    ticket_history = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'ticket_history': ticket_history})

# View for rendering the change password page
def change_password(request):
    return render(request, 'app/changepassword.html')

# View for rendering the mobile page
def mobile(request):
    return render(request, 'app/mobile.html')

# View for rendering the login page
# def login(request):
#     return render(request, 'app/login.html')

# change 
class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'app/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='theater').exists():
            return '/theater_dashboard/'  # Redirect to theater dashboard if user is in 'theater' group
        else:
            return '/profile/'  # Redirect to profile for other users

# View for customer registration
# class CustomerRegistrationView(View):
#     """
#     View for customer registration.

#     Methods:
#         get: Renders the customer registration form.
#         post: Processes the registration form submission and saves the new customer.
#     """

#     def get(self, request):
#         """
#         Render the customer registration form.

#         Args:
#             request: HttpRequest object containing metadata about the request.

#         Returns:
#             HttpResponse: Rendered customer registration form.
#         """
#         form = CustomerRegistrationForms()
#         return render(request, 'app/customerregistration.html', {'form': form})
  
#     def post(self, request):
#         """
#         Process the registration form submission and save the new customer.

#         Args:
#             request: HttpRequest object containing metadata about the request.

#         Returns:
#             HttpResponse: Rendered customer registration form with success message if form is valid,
#                           otherwise re-rendered customer registration form with errors.
#         """
#         form = CustomerRegistrationForms(request.POST)
#         if form.is_valid():
#             messages.success(request, 'Congratulations! Successfully Registered.')
#             form.save()
#         return render(request, 'app/customerregistration.html', {'form': form})

# change register
class CustomerRegistrationView(View):
    """
    View for customer registration.

    Methods:
        get: Renders the customer registration form.
        post: Processes the registration form submission and saves the new customer.
    """

    def get(self, request):
        """
        Render the customer registration form.

        Args:
            request: HttpRequest object containing metadata about the request.

        Returns:
            HttpResponse: Rendered customer registration form.
        """
        form = CustomerRegistrationForms()
        return render(request, 'app/customerregistration.html', {'form': form})
  
    def post(self, request):
        """
        Process the registration form submission and save the new customer.

        Args:
            request: HttpRequest object containing metadata about the request.

        Returns:
            HttpResponse: Rendered customer registration form with success message if form is valid,
                          otherwise re-rendered customer registration form with errors.
        """
        form = CustomerRegistrationForms(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            user.save()  # Save the user first
            if role == 'theater':
                theater_group = Group.objects.get(name='theater')
                user.groups.add(theater_group)
            messages.success(request, 'Congratulations! Successfully Registered.')
            return redirect('/accounts/login/')
        return render(request, 'app/customerregistration.html', {'form': form})
    
def checkout(request):
    """
    View for processing checkout.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse: Rendered checkout page with total amount and cart items.
    """
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    # Calculate CGST, SGST, and total amount
    CGST_rate = 8 / 100  # CGST rate of 8%
    SGST_rate = 5 / 100  # SGST rate of 5%
    total_amount = 0.0
    for item in cart_items:
        temp_amount = item.quantity * item.product.discounted_price
        CGST = temp_amount * CGST_rate  # Calculating CGST for the item
        SGST = temp_amount * SGST_rate  # Calculating SGST for the item
        total_amount += temp_amount + CGST + SGST  # Accumulating total amount for all items

    return render(request, 'app/checkout.html', {'total_amount': total_amount, 'cart_items': cart_items})

def payment_done(request):
    """
    View for processing payment and placing order.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponseRedirect: Redirects to the orders page after successful payment.
    """
    user = request.user
    custid = request.user.id
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)

    # Place order for each item in the cart and delete cart items
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()

    # Redirect to orders page after placing order
    return redirect("orders")

class ProfileView(View):  
    """
    View for handling user profile.

    Methods:
        get: Renders the profile page with the user's profile details.
        post: Handles form submission to update user profile.
    """

    def get(self, request):
        """
        Render the profile page with the user's profile details.

        Args:
            request: HttpRequest object containing metadata about the request.

        Returns:
            HttpResponse: Rendered profile page with user's profile details.
        """
        try:
            user_profile = Customer.objects.filter(user=request.user).first()
            if user_profile:
                form = CustomerProfileForm(instance=user_profile)
            else:
                form = CustomerProfileForm()
        except MultipleObjectsReturned:
            form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
  
    def post(self, request):
        """
        Handle form submission to update user profile.

        Args:
            request: HttpRequest object containing metadata about the request.

        Returns:
            HttpResponse: Rendered profile page with updated user profile details.
        """
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulation !!! Profile Updated Successfully.')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})