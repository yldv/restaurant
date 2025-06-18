from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from requests import Response
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
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


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

