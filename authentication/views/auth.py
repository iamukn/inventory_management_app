#!/usr/bin/python3
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

"""
   Endpoint to Login and Logout a user
"""

class Login(APIView):
    """
    Endpoint -> /auth/login
        Logs a user in, if the user is a registered user
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
            Authenticates and logs a user in
        Args:
            data(json) {'username': 'john doe', 'password': 'password'}
        Returns:
            data(json) 200 {'message': 'login successful'}
            data(json) 400 {'message': 'invalid username or password'}
        """
        try:
            # authenticate a user
            username = request.data.get('username')
            password = request.data.get('password')

            # check if the credentials were supplied
            if not username or not password:
                return Response({'message': 'username and password are required!'}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(**request.data)
        
            # logs a user in if user is not None

            if user is not None:
                login(request, user)
                return Response({'message': 'login successful'}, status=status.HTTP_200_OK)
            
            return Response({'message': 'invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle internal errors
        except Exception as e:
            print(e)
            return Response({'message': 'internal server error occurred!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Logout View
class Logout(APIView):
    """
    Endpoint -> /auth/logout

    """
    permission_classe = [IsAuthenticated]
    
    # logout 
    def get(self, request, *args, **kwargs):
        """
        GET -> Logs out a logged in user
        
        Args:
            request object

        Returns:
            200 (json)-> {'message': '<username> has been logged out'}
            401 (json)-> {'message': 'Authentication credentials were not provided.'}
        """
        
        if isinstance(request.user, AnonymousUser):
            return Response({'message': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        # log a user out
        user = request.user
        logout(request)

        return Response({'message': f'{user} has been logged out'})
