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
    
