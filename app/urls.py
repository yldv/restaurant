from django.urls import path
from .views import *

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('login_in/', login_in)
]