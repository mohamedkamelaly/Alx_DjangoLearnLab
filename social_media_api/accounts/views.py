from django.shortcuts import render
from .models import CustomUser
from .serializers import RegisterSerializer , LoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny , IsAuthenticated
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        # Check if the data passed in is valid.
        if serializer.is_valid():
            # If valid, save the user.
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        # If the data is invalid, return the errors.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        # Deserialize the incoming request data.
        serializer = LoginSerializer(data=request.data)
        # Validate the data.
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            # Use Django's built-in authentication system.
            user = authenticate(username=username, password=password)

            if user:
                # If authentication succeeds, return the token.
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            # If authentication fails, return an error.
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        # If the data is invalid, return the validation errors.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


