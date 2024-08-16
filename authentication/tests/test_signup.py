#!/usr/bin/python3
from authentication.tests.test_user import test_user
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# test the signup route
class SignupTest(APITestCase):
    # setup
    def setUp(self):
        self.user = test_user()

    def test_signup(self):
        url = reverse('signup')
        data = {"username": "johny", "email": "johndoe@cod.com", "password": "password"}
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
