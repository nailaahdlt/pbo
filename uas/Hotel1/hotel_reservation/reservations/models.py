from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
from django.utils.text import slugify

def room_images(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{slugify(instance.name)}.{ext}"
    return os.path.join('room_images/', filename)

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField()
    available_from = models.DateField()
    available_to = models.DateField()
    image = models.ImageField(upload_to=room_images, null=True, blank=True)
    def __str__(self):
        return f"{self.name} ({self.room_type})"

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')

    def clean(self):
        # Validasi agar kamar tidak dipesan lebih dari satu kali pada tanggal yang sama
        overlapping_reservations = Reservation.objects.filter(
            room=self.room,
            check_in_date__lt=self.check_out_date,
            check_out_date__gt=self.check_in_date
        )
        if overlapping_reservations.exists():
            raise ValidationError("Kamar ini sudah dipesan pada tanggal yang dipilih.")
            
    def __str__(self):
        return f"Reservation for {self.room.name} by {self.user.username}"