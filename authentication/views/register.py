#1/usr/bin/python3
from authentication.serializer import UserSerializer
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

class SignUp(APIView):
    """ Login route """

    def post(self, request, *args, **kwargs):
        
        """
        Registers a new user

        This endpoint receives a username, email, and password and registers the user to the database
        This Endpoint receives a POST request to the /signup endpoint

        Args:
            data (json): {"username": "john doe", "email": "johndoe@code.com", "password": "password"}

        Returns:
            
            data(json): 201 {"message": "registration successful", 'user': {<user info>}}
            data(json): 400 {"message": "ERROR MESSAGE"}
            data(json): 500 {'message':"INTERNAL SERVER ERROR MESSAGE"}
        """
        permission_classes = [AllowAny,]
        http_method_names = ['post']  # Only allow POST method

        try:
            data = request.data
            # create a user 
            with transaction.atomic():
                # Create and serialize a new user
                serializer = UserSerializer(data=data)
                

                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "registration successful", "user": serializer.data}, status=status.HTTP_201_CREATED)

                raise ValidationError(serializer.errors)


        except ValidationError as e:
            print(e) # can be logged to a file instead
            return Response({'message': str(e), 'status': 400})

        except Exception as e:
            print(e)
            return Response({'message': str(e), 'status': 500})
