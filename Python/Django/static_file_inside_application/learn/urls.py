from django.urls import path
from . import views

urlpatterns = [
    path('learn/', views.learn, name='learn'),
]