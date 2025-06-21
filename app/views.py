from datetime import time as booking_time

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
# Create your views here.

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
    responses={200: 'Booking successful'}
)
@api_view(['POST'])
def booking(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        table = serializer.validated_data['table']
        date = serializer.validated_data['date']
        time = serializer.validated_data['time']

        if table.is_reserved:
            return Response({'error': 'This table is already reserved'}, status=400)

        if not booking_time(9, 0) <= time <= booking_time(22, 0):
            return Response({'error': 'Booking only allowed between 09:00 and 22:00'}, status=400)

        user = request.user

        booking = Booking.objects.create(
            user=user,
            table=table,
            date=date,
            time=time,
            status='pending'
        )

        table.is_reserved = True
        table.save()

        return Response({'booking': f'{booking} Booking successful'}, status=200)

    return Response(serializer.errors, status=400)


@api_view(['POST'])
def cancel_booking(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)
    booking_id = request.data.get('booking_id')
    if not booking_id:
        return Response({'error': 'Booking ID required'}, status=400)
    booking = Booking.objects.filter(id=booking_id, user=request.user).first()
    if not booking:
        return Response({'error': 'Booking not found'}, status=404)
    booking.status = 'rejected'
    booking.save()
    booking.table.is_reserved = False
    booking.table.save()
    return Response({'booking': f'{booking} canceled successfully'}, status=200)


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

    return Response({'tables': serializer.data})

@api_view(['GET'])
def menu_list(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)
    menu = Menu.objects.select_related('category').prefetch_related('foods')
    serializer = MenuSerializer(menu, many=True)
    return Response(serializer.data, status=200)
