#!/usr/bin/python3
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from product.serializer import ProductsSerializer
from product.models import Products

""" Endpoints for GET PUT and DELETE of a product data
"""

class ProductDetailView(APIView):
    """
    Handles GET, PATCH, PUT, and DELETE for a single product.
    """
    # permissions
    def dispatch(self, request, *args, **kwargs):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]

        else:
            self.permission_classes = [IsAuthenticated]

        return super().dispatch(request, *args, **kwargs)

    # GET a product
    def get(self, request,id, *args, **kwargs):
        """
        This method handles GET requests to the `/products/<int:id>` endpoint and returns a dict of the product
        from the database. The endpoint is open to all users.

        Returns:
            A dictionary containing the product information

        Example:
            Response:
            {'name': 'John Doe', 'price': 99.45, 'quantity': 4, 'description': 'shoes'}
        """
        try:
            # get a product
            product = Products.objects.filter(id=id)
            # serialize all product
            if product:
                serializer = ProductsSerializer(product[0])
                # return the serialized data
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e) # can be logged into a file for debugging purposes
            return Response({'detail': 'an internal error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # update products
    def put(self, request,id, *args, **kwargs):
        """
        This method handles PUT requests to the `/products/<int:id>` endpoint and returns a dict of the updated product
        from he database. The endpoint is open to Admin Users ONLY
        
        Args:
            {'name': 'Johnny Doe', 'price': 92.45, 'quantity': 4, 'description': 'shoes'}
        Returns:
            A dictionary containing the updated product information
            -> 200 -> {'name': 'Johnny Doe', 'price': 92.45, 'quantity': 4, 'description': 'shoes'}
            -> 400 -> BAD REQUEST
            -> 500 -> {'detail': 'an internal error occurred'}

        """
        
        updated_data = request.data 
        try:
            # get the product using its ID
            product = Products.objects.filter(id=id)
            # serialize, update, and save the product
            if product:
                serializer = ProductsSerializer(product[0], data=updated_data)
                # return the updated data
                if serializer.is_valid():
                    serializer.save() 
                    return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # handle exception
        except Exception as e:
            print(e) # can be logged into a file for debugging purposes
            return Response({'detail': 'an internal error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # update products
    def patch(self, request,id, *args, **kwargs):
        """
        This method handles PATCH requests to the `/products/<int:id>` endpoint and returns a dict of the updated product
        from he database. The endpoint is open to Admin Users ONLY

        Args:
            {'name': 'Johnny Doe', 'price': 92.45, 'quantity': 4, 'description': 'shoes'}
        Returns:
            A dictionary containing the updated product information
            -> 200 -> {'name': 'Johnny Doe', 'price': 92.45, 'quantity': 4, 'description': 'shoes'}
            -> 400 -> BAD REQUEST
            -> 500 -> {'detail': 'an internal error occurred'}

        """

        updated_data = request.data

        try:
            # get the product using its ID
            product = Products.objects.get(id=id)
            # serialize, update, and save the product
            if product:
                serializer = ProductsSerializer(product, data=updated_data, partial=True)
                # return the updated data
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # handle exception
        except Exception as e:
            print(e) # can be logged into a file for debugging purposes
            return Response({'detail': 'an internal error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # delete a product

    def delete(self, request,id, *args, **kwargs):
        """
        This method handles DELETE requests to the `/products/<int:id>` endpoint and returns a dict of the updated product
        from he database. The endpoint is open to Admin Users ONLY
        
        Args:
            id of the product to delete
            DELETE -> /products/<int:id> 

        Response:
           status code 204 -> {'message': '<product name> deleted successfully!'}
           status code 404 -> NOT FOUND
        """
        try:
            product = Products.objects.get(id=id)
            # delete the product
            product.delete()

            return Response({'message': '%s deleted successfully!'%product.name},status=status.HTTP_204_NO_CONTENT)

        except Products.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
