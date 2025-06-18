from django.urls import path
from .views import *

urlpatterns = [
    path('register/', CreateUserAPIView.as_view()),
    path('login_in/', login_in),
    path('booking/', booking),
    path('list_bookings/', booking_list),
    path('api/tables/', table_list)
]