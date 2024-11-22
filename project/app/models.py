from django.db import models


class Client(models.Model):
    Email = models.EmailField(unique=True)
    username = models.TextField()
    phonenumber = models.IntegerField()
    password = models.TextField()
    location= models.TextField()

    def __str__(self):
        return self.username

class Advocate(models.Model):
    Email = models.EmailField(unique=True)
    name = models.TextField()
    phonenumber = models.IntegerField()
    password = models.TextField()
    location= models.TextField()
    bio=models.TextField()

    def __str__(self):
        return self.name
    
class Case(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Link complaint to the user
    advocate = models.ForeignKey(Advocate, on_delete=models.CASCADE)  # Link complaint to a police officer
    subject = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Case by {self.client.username} - {self.subject}"
