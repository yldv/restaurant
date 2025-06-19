from django.urls import path
from .views import *

urlpatterns = [
    path('register/', CreateUserAPIView.as_view()),
    path('login_in/', login_in),
    path('me/', me),
    path('booking/', booking),
    path('cancel/', cancel_booking),
    path('confirm/', confirm_booking),
    path('list_bookings/', booking_list),
    path('api/tables/', table_list)
]