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
            
            purchased_items = {}
            #return Response(serializer.data, status=status.HTTP_200_OK)

            for data in serializer.data:
                items = data.get('items')
                if items:

                    for item in items:
                        product = Products.objects.get(id=item.get('product_id'))
                        serializer = ProductsSerializer(product)
                        item_data = serializer.data

                        # add the data to the purchased_items
                        keys = (item_data['name'], item_data['id'])

                        if keys not in purchased_items or item['quantity'] > purchased_items[keys]['quantity']:
                            item_data['quantity'] = item['quantity']
                            purchased_items[keys] = item_data


            # convert the object to a dict
            unique_data = list(purchased_items.values())
            sorted_data = sorted(unique_data, key=lambda x: x.get('quantity'), reverse=True)
            return Response(sorted_data, status=status.HTTP_200_OK)
        return Response({"detail": "Access denied, please authenticate"},status=status.HTTP_403_FORBIDDEN)
