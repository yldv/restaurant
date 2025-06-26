from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['table', 'date', 'time', 'phone']

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'name', 'is_reserved']

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = ['id', 'name', 'category', 'price', 'picture']



class MenuSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    foods =  FoodSerializer(many=True)
    class Meta:
        model = Menu
        fields = ['id', 'category', 'foods']


class CancelBookingSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()
    class Meta:
        model = Booking
        fields = ['booking_id']