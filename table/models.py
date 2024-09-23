
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Category/')

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='food_items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='FoodItem/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# Model to store food items that are not submitted
class NotSubmittedItem(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='NotSubmitted/')
    # quantity = models.IntegerField(default=1)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.name} ({self.quantity})"


# Model to store submitted food items for billing
class SubmittedItem(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='Submitted/')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.total_price}"




