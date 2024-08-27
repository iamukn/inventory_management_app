#!/usr/bin/python3
from authentication.tests.test_user import test_user, admin_user
from django.urls import reverse
from product.models import Products
from order.models import Orders, OrdersItem
from rest_framework import status
from rest_framework.test import APITestCase


""" TEST ORDER VIEW"""

class OrderTest(APITestCase):

    def setUp(self):
        self.user = test_user()
        self.product = Products.objects.create(
            name="Adidas",
            price=25 * 100,
            description="shoes",
            quantity="21"
                )

        self.product.save()

        # create an order
        self.order = Orders.objects.create(
            user=self.user
                )

        self.order.save()

        self.ordersItem = OrdersItem.objects.create(
            order=self.order,
            product_id=self.product.id,
            quantity=5
                )

        self.ordersItem.save()





    def test_create_order(self):

        #login
        login_url = reverse('login')
        data = {"username": self.user.username, "password": "password"}
        login_res = self.client.post(login_url, data, format='json')

        url = reverse('orders')
        data = {"items": [{"product_id":1, "quantity": 5}]}

        response = self.client.post(url, data, format='json')
        # assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(type(response.json()), dict)
        self.assertTrue("total" in response.json())

    def test_check_order_status(self):
        login_url = reverse('login')
        data = {"username": self.user.username, "password": "password"}
        login_response = self.client.post(login_url, data, format='json')
        url = reverse('order-detail', kwargs={'id': self.order.id})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("pending" or "cancelled" or "completed" in response.json())

    def test_update__order_status(self):
        # make admin user 
        # login
        admin_user(self.user)
        login_url = reverse('login')
        data = {"username": self.user.username, "password": "password"}
        login_response =  self.client.post(login_url,data, format='json')

        url = reverse('order-detail', kwargs={'id': self.order.id})
        data = {"status": "completed"}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_salesreports(self):
        # login 
        admin_user(self.user)
        login_url = reverse('login')
        data = {"username": self.user.username, "password": "password"}
        login_response = self.client.post(login_url, data, format='json')
        #get sales reports
        url = reverse('salesreport')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue('daily_report' and 'weekly_report' and 'monthly_report' in res.json()) 

    def test_user_order_history(self):
        # login
        login_url = reverse('login')
        data = {"username": self.user.username, "password": "password"}
        login_response = self.client.post(login_url, data, format='json')
        #get order history
        url = reverse('order-history')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(type(res.json()) == list)
