#!/usr/bin/python3
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from order.serializer import OrderSerializer
from product.models import Products
from product.serializer import ProductsSerializer
from order.models import Orders

"""
    Return user orders, sorted by quantity
"""

class UserOrders(APIView):
    """
    Retrieve a list of orders created by a specific user, sorted by the largest quantity of products ordered.

    This endpoint takes a user ID from the request object as a parameter and returns a list of all orders associated with that user.
    Each order in the list is sorted by the quantity of products in descending order, starting with the largest quantity.

    Returns:
    Response: A JSON response containing a list of orders sorted by the largest quantity of products.
              Each order includes order details and the products ordered with their respective quantities.

    Example:
    GET /orders/sorted-by-quantity
    """
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        
        if not isinstance(request.user, AnonymousUser):
            orders = Orders.objects.filter(user=request.user)
            serializer = OrderSerializer(orders, many=True)
            
            purchased_items = []
            #return Response(serializer.data, status=status.HTTP_200_OK)

            for data in serializer.data:
                items = data.get('items')
                if items:

                    for item in items:
                        product = Products.objects.get(id=item.get('product_id'))
                        serializer = ProductsSerializer(product)
                        data = serializer.data

                        # add to the purchased_items 
                        purchased_items.append(data)
                        #s sort based on the quantity key

            

            product_dict = {}

            for product in purchased_items:
                key = (product["name"], product["id"])  # Use (name, id) as the unique key
                
                if key not in product_dict or product["quantity"] > product_dict[key]["quantity"]:
                    product_dict[key] = product

            # Convert the dictionary values to a list
            unique_products = list(product_dict.values())
        
            unique_products = sorted(unique_products, key= lambda x : x.get('quantity'), reverse=True)
            return Response(unique_products, status=status.HTTP_200_OK)
        return Response({"detail": "Access denied, please authenticate"},status=status.HTTP_403_FORBIDDEN)
