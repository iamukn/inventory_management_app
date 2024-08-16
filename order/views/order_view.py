#!/usr/bin/python3
from django.db import transaction
from order.serializer import OrderSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


# Create Order View
class OrderView(APIView):
    """
        Create order
        HTTP METHOD -> POST
    """
    
    def dispatch(self, request, *args, **kwargs):
        # updates permission
        if request.method != "POST":
            self.permission_classes = [IsAdminUser]

        self.permission_classes = [IsAuthenticated]
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # get the data from the request

        data = request.data

        with transaction.atomic():
            try:
            # serializer and validate the fields
                serializer = OrderSerializer(data=data)
                
        
                if serializer.is_valid():
                    serializer.save()
                    # remove the status
                    data=serializer.data
                    data.pop('status')

                    return Response(data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            #handle errors
            except Exception as e:
                raise e
                return Response({'message': 'an internal server error occurred!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
