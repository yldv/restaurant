from datetime import time as booking_time
from unicodedata import category
from urllib.parse import quote

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
# Create your views here.

#==================================================== DJANGO =============================================================================


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'username already exists'})
        user = User.objects.create(first_name=first_name, last_name=last_name, username=username, password=make_password(password), confirm_password=confirm_password, email=email)
        user.save()
        return redirect('/sign_in/')
    return render(request, 'register.html')


def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login_in.html', {'error': 'username or password is incorrect'})
    return render(request, 'login_in.html')

def logout_view(request):
    logout(request)
    return redirect('/sign_in/')


TELEGRAM_BOT_TOKEN = "8139875975:AAGC51DKfkAe0lk-pm2q92vKD2xc8TeiL_o"
TELEGRAM_CHAT_ID = "7025342701"
BASE_URL = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"


def booking(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'base_site.html', {'error': 'User not authenticated'}, status=401)

        serializer = BookingSerializer(data=request.POST)
        if serializer.is_valid():
            table = serializer.validated_data['table']
            date = serializer.validated_data['date']
            time = serializer.validated_data['time']
            phone = serializer.validated_data['phone']

            if table.is_reserved:
                return render(request, 'base_site.html', {'error': 'Table is already reserved'}, status=400)

            if not booking_time(9, 0) <= time <= booking_time(22, 0):
                return render(request, 'base_site.html', {'error': 'Booking only allowed between 09:00 and 22:00'}, status=400)

            booking = Booking.objects.create(
                user=request.user,
                table=table,
                date=date,
                time=time,
                status='pending',
                phone=phone
            )

            table.is_reserved = True
            table.save()

            text = f"New Reservation\nUser: {request.user.username}\nTable: {table.name}\nDate: {date}\nTime: {time}\nPhone: {phone}"
            encoded_text = quote(text)
            url = BASE_URL.format(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, encoded_text)
            requests.get(url)

            return render(request, 'base_site.html', {'booking': booking}, status=200)

        return render(request, 'base_site.html', {'error': serializer.errors}, status=400)

    tables = Table.objects.all()
    return render(request, 'base_site.html', {'table': tables})


def menu_list(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, 'menu.html', context={'error': 'User not authenticated'}, status=401)
        menu = Menu.objects.select_related('category').prefetch_related('foods')
        category = Category.objects.all()
        serializer = MenuSerializer(menu, many=True)
        foods = Foods.objects.filter(category__in=category)
        return render(request, 'menu.html', {'menu': serializer.data, 'category': category, 'foods': foods}, status=200)


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        message = request.POST.get("message")

        obj = Contact.objects.create(name=name, email=email, number=number, message=message)
        obj.save()
        res = requests.get(BASE_URL.format(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
                                                    f"name: {name} \nemail: {email} \nnumber: {number} \nmessage:{message}"))
        return redirect('/')
    return render(request, "contact.html")



#=================================================== SWAGGER ========================================================================================

class CreateUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={200: UserSerializer(many=True)}
)
@api_view(['POST'])
def login_in(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.filter(username=username).first()
    if not user:
        return Response({'error': 'User not found'}, status=404)

    if not user.check_password(password):
        return Response({'error': 'password incorrect'}, status=403)


    return Response({'user': f'{username} Login successful'}, status=200)


@swagger_auto_schema(
    method='post',
    request_body=BookingSerializer,
    responses={200: BookingSerializer(many=True)}
)
@api_view(['POST'])
def booking_swagger(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        table = serializer.validated_data['table']
        date = serializer.validated_data['date']
        time = serializer.validated_data['time']
        phone = serializer.validated_data['phone']
        if table.is_reserved:
            return Response({'error': 'Table is already reserved'}, status=400)
        if not booking_time(9, 0) <= time <= booking_time(22, 0):
            return Response({'error': 'Booking only allowed between 09:00 and 22:00'}, status=400)

        table.is_reserved = True
        table.save()

        return Response({'booking': serializer.data}, status=200)
@swagger_auto_schema(
    method='post',
    request_body=CancelBookingSerializer,
    responses={200: CancelBookingSerializer(many=True)}
)
@api_view(['POST'])
def cancel_booking(request):
    if not request.user.is_staff:
        return Response({'error': 'Only admins can cancel bookings'}, status=403)

    serializer = CancelBookingSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    booking_id = serializer.validated_data['booking_id']
    booking = Booking.objects.filter(id=booking_id).first()
    if not booking:
        return Response({'error': 'Booking not found'}, status=404)

    booking.status = 'rejected'
    booking.save()

    booking.table.is_reserved = False
    booking.table.save()

    return Response({'message': f'Booking #{booking_id} cancelled successfully'}, status=200)


@api_view(['POST'])
def confirm_booking(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)
    if not request.user.is_staff:
        return Response({'error': 'Only admins can confirm bookings'}, status=403)
    booking_id = request.data.get('booking_id')
    if not booking_id:
        return Response({'error': 'Booking ID is required'}, status=400)
    booking = Booking.objects.filter(id=booking_id).first()
    if not booking:
        return Response({'error': 'Booking not found'}, status=404)
    booking.status = 'accepted'
    booking.save()
    booking.table.is_reserved = True
    booking.table.save()
    return Response({'message': f'Booking {booking.id} confirmed'}, status=200)


@api_view(['GET'])
def me(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)
    serializer = UserSerializer(request.user)
    return Response({'user': serializer.data}, status=200)


@api_view(['GET'])
def booking_list(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)
    list = Booking.objects.filter(user=request.user).order_by('-date')
    serializer = BookingSerializer(list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def table_list(request):
        if not request.user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=401)
        table = Table.objects.all()
        serializer = TableSerializer(table, many=True)
        return Response({'table': serializer.data}, status=200)


@api_view(['GET'])
def menu_list_swagger(request):
       if not request.user.is_authenticated:
           return Response({'error': 'User not authenticated'}, status=401)
       menu = Menu.objects.select_related('category').prefetch_related('foods')
       category = Category.objects.all()
       serializer = MenuSerializer(menu, many=True)
       foods = Foods.objects.filter(category__in=category)
       return Response({'menu': serializer.data}, status=200)
@swagger_auto_schema(
    method='post',
    request_body=FoodSerializer,
    responses={200:FoodSerializer(many=True)},
)
@api_view(['POST'])
def add_food(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)
    if not request.user.is_staff:
        return Response({'error': 'Only admins can add foods'}, status=403)
    serializer = FoodSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
