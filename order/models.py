from django.db import models
from django.contrib.auth.models import User

""" The Order model """
class Orders(models.Model):
    #products = models.JSONField(default=list)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="pending")
    date_of_purchase = models.DateField(auto_now_add=True)
    total = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.id}" 

class OrdersItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items')
    product_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Product: {self.product_id} Quantity: {self.quantity}"

