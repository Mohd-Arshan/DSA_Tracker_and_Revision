from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
# Create your views here.


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "User registered successfully"
        },status=status.HTTP_201_CREATED)
 
        
class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        access_token = serializer.validated_data['access']
        refresh_token = serializer.validated_data['refresh']
        user = serializer.validated_data['user']
        
        response = Response({
            'message': 'Login successful',
            'user': user
        }, status=status.HTTP_200_OK)
        
        # Set the access token in an HttpOnly cookie
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production
            samesite='Lax'  # Adjust as needed
        )
        
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=False,  # Set to True in production
            samesite='Lax'  # Adjust as needed
        )
        
        return response
        
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        user.token_version += 1  # Increment token version to invalidate existing tokens
        user.save()
        
        response = Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
        
        # Clear the access and refresh tokens from cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'username': user.username
        }, status=status.HTTP_200_OK)
        