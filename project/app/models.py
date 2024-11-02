from django.contrib.auth.models import User
from django.db import models

class Advocate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    bio = models.TextField()
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Booking(models.Model):
    advocate = models.ForeignKey(Advocate, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client")
    booking_date = models.DateField()
    details = models.TextField()

    def __str__(self):
        return f"Booking by {self.client.username} with {self.advocate.user.username}"
