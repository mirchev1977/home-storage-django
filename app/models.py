from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=50)
    token = models.CharField(max_length=2000, null=True)


class UserLogged(models.Model):
    token = models.CharField(max_length=1000, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              name = "owner")
    createdAt = models.CharField(max_length=255,
                                 null=True, name="created_at")


class Location(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                name = "creator")
    imgUrl = models.CharField(max_length=3000, null=True, name='img_url')
    location = models.CharField(max_length=255, null=True)
    privacy = models.CharField(max_length=30, null=True)


class Container(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                name="creator")
    location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 name='location')
    description = models.CharField(null=True, max_length=2000)
    vertical = models.CharField(max_length=255, null=True)
    items = models.CharField(max_length=2000, null=True)
    privacy = models.CharField(max_length=40)
    imgLink = models.CharField(max_length=1000, null=True,
                               name="img_link")
    url = models.CharField(max_length=1000, null=True,
                           name="url")
    coords = models.CharField(max_length=255, null=True)


class Item(models.Model):
    description = models.CharField(max_length=1000, null=True)
    imgUrl = models.CharField(max_length=1000, null=True,
                              name="img_url")
    container = models.ForeignKey(Container, on_delete=models.CASCADE,
                                  name="container")
