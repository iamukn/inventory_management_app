#!/usr/bin/python3
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import status
from order.models import Orders
from product.models import Products

""" Orders Serializer """
class OrderSerializer(ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"
        depth: 1


    def validate(self, data):
        # check if the status is either pending, completed or cancelled
        if 'products' in data:
            return data

        elif 'status' in data:
            if data.get('status') not in ['pending', 'completed', 'cancelled']:
                raise ValidationError({"error": "status must be either pending, completed or cancelled"})

        return data
    

    def to_internal_value(self, data):
        orders = super().to_internal_value(data)
        total = 0
        # check if the data contains data
        if orders.get('products'):
            # fetch the price of each products
            for order in orders['products']:
                id = order.get('id')
                product = Products.objects.get(id=id)
                price = product.price / 100
                quantity = order.get('quantity')
                price = price * quantity
                total += price

                # subtract the quantity from the stock
                new_quantity = product.quantity - quantity
                if new_quantity >= 0:
                    product.quantity = new_quantity
                    product.save()
                

            # update the total with the total price
            orders['total'] = total

        return orders
