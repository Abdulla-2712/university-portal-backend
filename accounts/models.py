from django.db import models

# Create your models here.



class Student(models.Model):
    id = models.AutoField(primary_key=True)
    Seat_Number = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    profile_photo = models.ImageField(upload_to='profile_photos_student/', null=True, blank=True)
    department = models.CharField(max_length=10)
    level = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    