#!/usr/bin/python3
from authentication.tests.test_user import test_user, admin_user
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

"""
    Test create and retrieve products
"""

class ProductTest(APITestCase):
    # setup
    def setUp(self):
        self.user = test_user()
    
    # test retrieve products open to all users
    def test_retrieve_products(self):
        login_url = reverse('login')
        user_data = {"username": self.user.username, "password": "password"}
        response = self.client.post(login_url, user_data, format='json')

        url = reverse('products')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(type(res.json()), list)
    
    # test create product open to ADMIN users only
    def test_create_product(self):
        
        # make the user an admin user
        admin_user(self.user)

        # login as an admin user
        login_url = reverse('login')
        user_data = {"username": self.user.username, "password": "password"}
        response = self.client.post(login_url, user_data, format='json')

        # test create
        url = reverse('products')
        data = {
            "name": "Adidas AirForce1",
            "description": "Footwear",
            "quantity": 45,
            "price": 100,
                }
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
