from rest_framework import generics, viewsets
from rest_framework.decorators import api_view ,permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user_app.api.serializers import *
from user_app.models import Profile

from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from django.db.models import Q
import jwt
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema 

from rest_framework.generics import ListAPIView , CreateAPIView, UpdateAPIView,DestroyAPIView

from rest_framework_simplejwt.tokens import RefreshToken


# Helper function to generate JWT token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    my_tags = ["Profile"]
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)  # Generate JWT tokens for user
            return Response(tokens, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    my_tags = ["Profile"]
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                tokens = get_tokens_for_user(user)  
                return Response(tokens, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                                  
                                  
                                  
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    my_tags = ["Profile"]



class PasswordChangeView(APIView):
    my_tags = ["Profile"]

    @swagger_auto_schema(
        request_body=PasswordChangeSerializer,
        responses={
            200: "Password changed successfully",
            400: "Bad Request",
           
        },
    )
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            userSelecte = Profile.get_user_jwt(self , request).user
            # Validate old and new passwords using Django's PasswordChangeForm
            form = PasswordChangeForm(userSelecte, serializer.validated_data)
            if form.is_valid():
                # Save the new password
                form.save()
                return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        
       
        
       
