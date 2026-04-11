from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=50)

class Bus(models.Model):
    name=models.CharField(max_length=50)
    source=models.CharField(max_length=50)
    destination=models.CharField(max_length=50)
    price=models.IntegerField()

class Booking(models.Model):
    username=models.CharField(max_length=50)
    bus=models.CharField(max_length=50)
    seats=models.CharField(max_length=100)
    passenger_name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=15)