from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name



class Foods(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    rating = models.IntegerField()
    def __str__(self):
        return self.name


class Menu(models.Model):
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Table(models.Model):
    name = models.CharField(max_length=100)
    foods = models.ManyToManyField(Foods)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100)
    foods = models.ManyToManyField(Foods)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name