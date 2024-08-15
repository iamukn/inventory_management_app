#!/usr/bin/python3
from django.db import transaction
from order.models import Orders
from order.serializer import OrderSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status


# Create Order View
class OrderDetailView(APIView):
    """
        Retrieve and update the status of an order
        HTTP METHOD -> [GET, PATCH]
    """

    def dispatch(self, request, *args, **kwargs):
        # updates permission
        if request.method != "GET":
            self.permission_classes = [IsAdminUser]

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id, *args, **kwargs):
        """
            GET -> Retrieves the status of an order
                path -> /orders/<id:int>/status 
            
            Example:
               GET  -> /orders/1/status
            Returns:
                200 json data -> {"id": int, "status": str}
                400 json data -> {"message": "order id is invalid!"}
                500 json data -> {"message": "an internal server error occurred!"}
        """        
        try:
            # fetch an order using its id
            order = Orders.objects.get(id=id)
            serializer = OrderSerializer(order)
            data = serializer.data
            order_status = {"id": data.get('id'), "status": data.get('status')}

            return Response(order_status, status=status.HTTP_200_OK)
        
        except Orders.DoesNotExist as e:
            print(e) # can log to a file
            return Response({"message": "order id is invalid!"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': 'an internal server error occurred!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, id, *args, **kwargs):
        """
        PATCH -> Updates the status of an order
        permission -> ADMIN ONLY

        Args:
            required: -> json data {'status': "completed" or "cancelled" or "pending"}

        Returns: 200 -> json data {'message': 'update successful','id': int, 'status': <updated status word>}
                 400 -> 
                    - json data -> {"message": "order id is invalid!"}
                    - json data -> {"message": {"errors": [strings of errors]}}
                 500 json data -> {"message": "an internal server error occurred!"}
        """
        # get the request data
        order_status = request.data

        # get the order
        try:
            
            order = Orders.objects.get(id=id)
            serializer = OrderSerializer(order, data=order_status, partial=True)
            if serializer.is_valid():
                serializer.save()

                # data
                data = serializer.data

                return Response({'message': 'update successful','id': data.get('id'), 'status': data.get('status')}, status=status.HTTP_200_OK)
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Orders.DoesNotExist:
            return Response({"message": "order id is invalid!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'an internal server error occurred!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
