from django.urls import path,register_converter
from enroll import views,converter

register_converter(converter.FourDigitYearConverter,'yyyy')

urlpatterns=[
    path('session/<yyyy:year>/',views.showDetail,name="detail"),
]