from django.urls import path
from enroll import views

urlpatterns=[
    # path('student/<my_id>/',views.showDetail,name="detail"),
    path('student/<int:my_id>/',views.showDetail,name="detail"),
    path('student/<int:my_id>/<int:my_subid>/',views.showSubDetail,name="subdetail"),
]