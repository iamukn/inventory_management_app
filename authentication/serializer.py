#!/usr/bin/python3
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

# Create a User serializer
class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = "__all__"
        depth = 1
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure the password is write-only
        }


    def create(self, validated_data):
        # extract the password
        password = validated_data.get('password')

        # create a user
        user = User(**validated_data)

        # set password
        user.set_password(password)

        # save the instance
        user.save()

        # return the user
        return user

    def to_representation(self, instance):
        # Dynamically exclude certain fields
        representation = super().to_representation(instance)
        representation.pop('is_staff', None)
        representation.pop('is_superuser', None)
        representation.pop('date_joined', None)
        representation.pop('groups', None)
        representation.pop('user_permissions', None)
        return representation
