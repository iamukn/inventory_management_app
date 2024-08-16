#!/usr/bin/python3
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.tests.test_user import test_user

class LoginTest(APITestCase):
    # test user
    def setUp(self):
        self.user = test_user()


    def test_login(self):
        """ test the login route """
        url = reverse('login')
        data = {"username": self.user.username, "password": "password"}
        response = self.client.post(url, data, format='json')
        json = response.json()

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(json.get('message'), "login successful")


    def test_logout(self):
        """ test the logout route """
        
        # login 
        login_url = reverse('login')
        data = {"username": self.user.username, "password": "password"}
        login_res = self.client.post(login_url, data, format='json')

        # logout
        url = reverse('logout')
        response = self.client.get(url)
        json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.get('message'),"%(user)s has been logged out"%{"user": self.user.username})
