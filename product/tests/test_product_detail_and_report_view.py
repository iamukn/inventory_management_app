#!/usr/bin/python3                                                                                                                                           [25/1625]from authentication.tests.test_user import test_user
from authentication.tests.test_user import test_user, admin_user
from django.urls import reverse
from rest_framework import status
from product.models import Products
from rest_framework.test import APITestCase

"""
    Test product detail view
"""

class ProductTest(APITestCase):
    # setup
    def setUp(self):
        # create a product
        self.product = Products.objects.create(
            name='Adidas',
            description="foot wear",
            price=25 * 100,
            quantity=20,
                )

        self.product.save()
        # instantiate a test user
        self.user = test_user()

    def test_get_product(self):
        #login
        login_url = reverse('login')
        user_data = {"username": self.user.username, "password": "password"}
        response = self.client.post(login_url, user_data, format='json')
        # fetch a product with a unique id
        url = reverse('product', kwargs={'id': self.product.id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(type(res.json()), dict)

    
    def test_put_product(self):
        #make admin user
        admin_user(self.user)

        login_url = reverse('login')
        login_data = {"username": self.user.username, "password": "password"}
        login_response = self.client.post(login_url, login_data, format='json')

        # update a product with a unique id
        url = reverse('product', kwargs={'id': self.product.id})
        data = {'name': 'Adidas Shoe', 'description': 'foot wear', 'quantity': 10, 'price': 45}
        res = self.client.put(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get('name'),res.json().get('name'))

    def test_patch_product(self):
        # make admin user
        admin_user(self.user)

        login_url = reverse('login')
        login_data = {"username": self.user.username, "password": "password"}
        login_response = self.client.post(login_url, login_data, format='json')

        #update a product with a unique id
        url = reverse('product', kwargs={'id': self.product.id})
        data = {'quantity': 1}
        res = self.client.patch(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get('quantity'),res.json().get('quantity'))
    
    def test_delete_product(self):
        # make admin user
        admin_user(self.user)

        #login 
        login_url = reverse('login')
        login_data = {"username": self.user.username, "password": "password"}
        login_response = self.client.post(login_url, login_data, format='json')
        #delete a product
        url = reverse('product', kwargs={'id': self.product.id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
