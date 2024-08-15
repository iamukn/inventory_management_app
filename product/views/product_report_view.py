#!/usr/bin/python3
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from product.models import Products
from product.serializer import ProductsSerializer

""" Product reporting endpoints """
class ProductsReportView(APIView):
    """
        GET -> Inventory report of all products with low stock
    """

    permission_classes = [IsAdminUser,]

    def get(self, request, *args, **kwargs):
        """
        Returns a list of products with stocks less than 10

        Returns:
            200 -> json {'products':[{{object}, {object}, 'count': int}]
        """
        try:
            products = Products.objects.filter(quantity__lt=10)
            serializer = ProductsSerializer(products, many=True)
            data = serializer.data

            return Response({'count': len(data),'products': data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e) # log in a file
            return Response({'message': 'an internal error occurred!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
