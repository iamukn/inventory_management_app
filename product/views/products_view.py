#!/usr/bin/python3
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from product.serializer import ProductsSerializer
from product.models import Products

""" Endpoints for GET POST PUT and DELETE of the product data
"""

class Products_view(APIView):
    """
    Endpoints for GET POST of the product data
    """
    # permissions
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            self.permission_classes = [IsAdminUser]
        
        else:
            self.permission_classes = [AllowAny]

        return super().dispatch(request, *args, **kwargs)

    # GET all products
    def get(self, request, *args, **kwargs):
        """
        This method handles GET requests to the `/products/` endpoint and returns a list of all products
        available in the database. The endpoint is open to all users.

        Returns:
            A list of dictionaries containing all the products

        Example:
            Response:
            [
            {'name': 'John Doe', 'price': 99.45, 'quantity': 4, 'description': 'shoes'}.
            {'name': 'Jane Doe', 'price': 9.45, 'quantity': 3, 'description': 'pen'}.
            ]   
        """
        try:
            # get all products
            products = Products.objects.all()
            # serialize all products
            serializer = ProductsSerializer(products, many=True)
            # return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e) # can be logged into a file for debugging purposes
            return Response({'detail': 'an internal error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # Add a product

    def post(self, request, *args, **kwargs):
        """ 
        Creates a new product
        -> POST /products/
        Args:
            -> json data - {"name": "shoes", "description": "footwears", "quantity": 3, "price": 9.25}
        Returns:
            -> json data 200 - {"status": "created", "name": "shoes", "description": "footwears", "quantity": 3, "price": 9.25}
        """

        product = request.data
        
        # convert price to an integer
        try:
            with transaction.atomic():
                # serialize the product data
                serializer = ProductsSerializer(data=product)
                print(product)
        
                # check if the product is valid
                if serializer.is_valid():
                    serializer.save()

                    return Response({"status": "created", **serializer.data}, status=status.HTTP_201_CREATED)
            
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'message': 'an internal server error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
