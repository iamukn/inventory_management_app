#!/usr/bin/python3
from rest_framework.serializers import ModelSerializer, ValidationError
from product.models import Products

# Serializer for the products
class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"
        depth = 1

   

    def validate(self, data):

        """
        Validate the data before saving.
        """
        if 'price' in data and data['price'] < 0:
            raise serializers.ValidationError({'price': 'Price must be greater than or equal to zero'})
        
        # Ensure that there's a name in the dict
        if 'name' in data and not data['name']:
            raise serializers.ValidationError({'name': 'Name cannot be empty'})
        return data
   
    def update(self, instance, data):
        # update the instance

        instance.price = data.get('price', instance.price)
        instance.name = data.get('name', instance.name)
        instance.quantity = data.get('quantity', instance.quantity)
        instance.description = data.get('description', instance.description)

        # save and return the instance
        instance.save()
        return instance

    # updates the product price to price with decimal before sending to the client
    def to_representation(self, instance):
        product_data = super().to_representation(instance)
        product_data['price'] = "%s%s"%("$", product_data.get('price') / 100)
        return product_data

    
    # validate the data sent from the client side
    def to_internal_value(self, data):
        # check if price is in the data
        if data.get('price'):
            data['price'] = data['price'] * 100
        data = super().to_internal_value(data)

        return data
