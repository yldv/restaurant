from django.db import models
from django.contrib.auth.models import User


# Create your models here.
STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)


class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name



class Foods(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    def __str__(self):
        return self.name


class Menu(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    foods = models.ForeignKey(Foods, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name


class Table(models.Model):
    name = models.CharField(max_length=100)
    is_reserved = models.BooleanField(default=False)
    capacity = models.IntegerField(default=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name




class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('table', 'date', 'time')

    def __str__(self):
        return self.table.name