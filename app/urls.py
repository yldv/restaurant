from aiogram.types import contact
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', CreateUserAPIView.as_view()),
    path('login_in/', login_in),
    path('me/', me),
    path('', booking),
    path('cancel/', cancel_booking),
    path('confirm/', confirm_booking),
    path('list_bookings/', booking_list),
    path('tables/', table_list),
    path('menu/', menu_list),
    path('add_food/', add_food),
    path('contact/', contact_view),
    path('booking_swagger/', booking_swagger),
    path('menu_swagger/', menu_list_swagger),
    path('sign_up/', signup_view),
    path('sign_in/', signin_view),
    path('logout/', logout_view),

]