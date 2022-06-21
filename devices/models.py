from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Room(models.Model):
    name = models.TextField(max_length=255)
    def __str__(self) -> str:
        return f"{self.name} ({self.id})"
    def get_absolute_url(self):
        return reverse('devices', kwargs={"roomId": self.id})
    
class Device(models.Model):
    pin = models.IntegerField()
    name = models.TextField(max_length=255)
    status = models.BooleanField()
    last_Active = models.DateTimeField(blank=True, null=True)
    room = models.ForeignKey(Room,on_delete=models.CASCADE,
                             )

    def __str__(self) -> str:

        return f"{self.room}: {self.name} {self.pin}"

class Door_Infomation(models.Model):
    status = models.BooleanField()
    time = models.DateTimeField()
    user = models.ForeignKey(User, related_name="opener", null=True, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='documents', null = True)