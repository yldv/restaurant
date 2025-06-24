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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    picture = models.URLField(default='https://www.google.com/imgres?q=food&imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F6%2F6d%2FGood_Food_Display_-_NCI_Visuals_Online.jpg%2F1200px-Good_Food_Display_-_NCI_Visuals_Online.jpg&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FFood&docid=F4fzcSFVcTK1kM&tbnid=nQBYUAp94s8s4M&vet=12ahUKEwjJkY3XpIiOAxU9U1UIHcC-CdMQM3oECBoQAA..i&w=1200&h=800&hcb=2&ved=2ahUKEwjJkY3XpIiOAxU9U1UIHcC-CdMQM3oECBoQAA')
    description = models.TextField()
    def __str__(self):
        return self.name


class Menu(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    foods = models.ManyToManyField(Foods)

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
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('table', 'date', 'time')

    def __str__(self):
        return self.table.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.IntegerField()
    message = models.TextField()
    def __str__(self):
        return f"{self.name} - {self.email}"