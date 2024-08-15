#!/usr/bin/python3
from django.urls import path
from authentication.views.register import SignUp
from authentication.views.auth import Login, Logout
# Url pattern for the Auth route

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    path('auth/login', Login.as_view(), name='login'),
    path('auth/logout', Logout.as_view(), name='logout'),
        ]
