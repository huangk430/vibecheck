#create database tables
from django.db import models
from django.contrib.auth.models import User

class AccessToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150, blank=True)
    expiration = models.DateTimeField()

class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f"{self.name} ({self.id})"
    
class Vibe(models.Model):
    name = models.CharField(max_length=20)
    genres = models.ManyToManyField(Genre)
    def __str__(self):
        return f"{self.name.upper()} ({self.id}): {', '.join([str(g) for g in self.genres.all()])}"

class UserVibe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vibe = models.ForeignKey(Vibe, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)


