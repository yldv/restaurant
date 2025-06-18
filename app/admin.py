from django.contrib import admin
from .models import Table, Category, Booking, Foods, Menu
# Register your models here.

admin.site.register(Table),
admin.site.register(Category),
admin.site.register(Booking),
admin.site.register(Foods),
admin.site.register(Menu)
