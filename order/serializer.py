#!/usr/bin/python3
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import status
from order.models import Orders, OrdersItem
from product.models import Products

""" Orders Serializer """

class OrdersItemSerializer(ModelSerializer):
    class Meta:
        model = OrdersItem
        fields = ['id', 'product_id', 'quantity']




class OrderSerializer(ModelSerializer):
    # nested serializer
    items = OrdersItemSerializer(many=True)

    class Meta:
        model = Orders
        fields = "__all__"
        depth: 1

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Orders.objects.create(status='pending', **validated_data)
        for item_data in items_data:
            OrdersItem.objects.create(order=order, **item_data)
        return order


    def validate(self, data):
        # check if the status is either pending, completed or cancelled
        if 'items' in data:
            return data

        elif 'status' in data:
            if data.get('status') not in ['pending', 'completed', 'cancelled']:
                raise ValidationError({"error": "status must be either pending, completed or cancelled"})

        return data
    

    def to_internal_value(self, data):
        orders = super().to_internal_value(data)
        total = 0
        # check if the data contains data
        if orders.get('items'):
            # fetch the price of each products
            for order in orders['items']:
                id = order.get('product_id')
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

    def to_representation(self, instance):
        res = super().to_representation(instance)

        res.pop('user')

        return res
