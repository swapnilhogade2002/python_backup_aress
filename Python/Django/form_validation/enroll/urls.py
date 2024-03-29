from django.urls import path
from . import views

urlpatterns = [
    path("validate/",views.showFormData),
    path("success/",views.thanks)
]
