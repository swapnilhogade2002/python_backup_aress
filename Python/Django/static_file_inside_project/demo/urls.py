from django.urls import path
from . import views  # Import views module


urlpatterns = [
    path('learn/', views.learn),  # Reference the learn view function
]
