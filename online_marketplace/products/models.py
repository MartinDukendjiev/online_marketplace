from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/categories/', null=True, blank=True)

    def __str__(self):
        return self.name


# class SubCategory(models.Model):
#     name = models.CharField(max_length=200)
#     category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name


class Product(models.Model):
    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Used', 'Used'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    upload_date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    # subcategory = models.ForeignKey(SubCategory, related_name='products', null=True, blank=True, on_delete=models.SET_NULL)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='New')
    image = models.ImageField(upload_to='static/products/', null=True, blank=True)

    def __str__(self):
        return self.name
