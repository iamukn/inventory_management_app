#!/usr/bin/python3
from django.contrib.auth.models import User

def test_user():
    user = User.objects.create_user(
        username="john",
        email="johndoe@code.com",
        first_name="john",
        last_name="doe"
        )
    user.set_password("password")
    user.save()
    return user

def admin_user(user):
    user.is_staff = True
    user.is_superuser = True
    user.save()
