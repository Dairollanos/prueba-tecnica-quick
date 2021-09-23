from django.contrib.auth.models import User
from django.db import models


# El campo "username" sirve para relacionar a la persona regisrada con un usuario en Django
class Users(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_birth = models.DateField()
    address = models.CharField(max_length=50)
    token = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=120)
    mobile_phone = models.CharField(max_length=25)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name

