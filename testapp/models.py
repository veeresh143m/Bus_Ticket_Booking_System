from django.db import models

# Create your models here.
# class User(models.Model):
#     username=models.CharField(max_length=50)
#     email=models.EmailField()
#     password=models.CharField(max_length=50)
#
# class Bus(models.Model):
#     name=models.CharField(max_length=50)
#     source=models.CharField(max_length=50)
#     destination=models.CharField(max_length=50)
#     price=models.IntegerField()
#
# class Booking(models.Model):
#     username=models.CharField(max_length=50)
#     bus=models.CharField(max_length=50)
#     seats=models.CharField(max_length=100)
#     passenger_name=models.CharField(max_length=50)
#     mobile=models.CharField(max_length=15)

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# =========================
# BUS MODEL
# =========================
class Bus(models.Model):
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.IntegerField()
    total_seats = models.IntegerField(default=40)

    def __str__(self):
        return f"{self.name} ({self.source} → {self.destination})"


# =========================
# SEAT MODEL
# =========================
class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.IntegerField()

    is_booked = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bus.name} - Seat {self.seat_number}"

    class Meta:
        unique_together = ['bus', 'seat_number']   # 🚀 Prevent duplicates


# =========================
# BOOKING MODEL
# =========================
class Booking(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)

    passenger_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.status}"


# =========================
# SEAT LOCK MODEL
# =========================
class SeatLock(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seat} locked by {self.user}"


# =========================
# AUTO CREATE SEATS (🔥 IMPORTANT)
# =========================
@receiver(post_save, sender=Bus)
def create_seats(sender, instance, created, **kwargs):
    if created:
        for i in range(1, instance.total_seats + 1):
            Seat.objects.create(
                bus=instance,
                seat_number=i
            )