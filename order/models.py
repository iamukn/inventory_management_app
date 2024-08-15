from django.db import models

""" The Order model """
class Orders(models.Model):
    products = models.JSONField(default=list)
    status = models.CharField(max_length=20, default="pending")
    date_of_purchase = models.DateField(auto_now_add=True)
    total = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.id}" 
