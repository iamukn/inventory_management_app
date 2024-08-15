#!/usr/bin/python3

from django.db import models

""" Product database schema """

class Products(models.Model):
    # product fields
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField()

    def __str__(self):
        return str(self.name)
