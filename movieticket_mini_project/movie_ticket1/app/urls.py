from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MysetPasswordForm
# from .views import CustomLoginView

urlpatterns = [
    # path('', views.home),
    path('',views.MoviesView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.MoviesDetailView.as_view(), name='product-detail'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.show_cart, name='showcart'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('generate-ticket-pdf/<int:order_id>/', views.generate_ticket_pdf, name='generate_ticket_pdf'),
    path('book_tickets/', views.book_tickets, name='book_tickets'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    
    path('passwordchange/', 
         auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html'
                                               ,form_class= MyPasswordChangeForm
                                               ,success_url='/passwordchangedone'
                                               ),
         name='passwordchange'),
    path('passwordchangedone/',
         auth_views.PasswordChangeView.as_view(
             template_name='app/passwordchangedone.html'
         ),
         name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(
        template_name='app/password_reset.html') ,name='password_reset'),
    
    path('password-reset-done/',auth_views.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html') ,name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html') ,name='password_reset_confirm'),
    
    path('password-reset-complete/',auth_views.PasswordResetDoneView.as_view(
    template_name='app/password_reset_complete.html') ,name='password_reset_complete'),
    # path('movie/<slug:data>', views.mobile, name='movie'),
    
    path('movie/', views.thriller_sort, name='thriller_sort'), 
    path('movie-entertain/', views.entertaintment_sort, name='entertainrmovie'),
    path('movie-romance/', views.romantic_sort, name='romanticrmovie'),
    # path('login/', views.login, name='login'),

    # path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',
    #                                                      authentication_form=LoginForm)
    #      , name='login'),
    path('login/', views.custom_login, name='login'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    
    # login to different dashboard
    # path('accounts/login/', CustomLoginView.as_view(), name='login'),

    # path('theater-dashboard/', views.theater_dashboard, name='theater_dashboard'),
    # path('user-dashboard/', views.MoviesView.as_view(), name='normal_dashboard'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

# theater dashboard
path('addmovie/', views.add_movie, name='addmovie'),
path('show-movie/', views.MoviesViewTheater.as_view(), name='moviesviewtheater'),
path('edit-movie/<int:pk>/', views.EditMovieView.as_view(), name='edit-movie'),
path('delete-movie/<int:pk>/', views.DeleteMovieView.as_view(), name='delete-movie'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
