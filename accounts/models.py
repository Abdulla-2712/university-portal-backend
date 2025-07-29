from django.db import models

# Create your models here.



class Student(models.Model):
    id = models.AutoField(primary_key=True)
    Seat_Number = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True )
    password = models.CharField(max_length=128)  
    # profile_photo = models.ImageField(upload_to='profile_photos_student/', null=True, blank=True)
    department = models.CharField(max_length=30)
    level = models.CharField(max_length=20)
    password_reset_token = models.CharField(max_length=128, null=True, blank=True)
    reset_token_created_at = models.DateTimeField(null=True, blank=True)



class Registration_Request(models.Model):
    id = models.AutoField(primary_key=True)
    Seat_Number = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    # student_id_card = models.ImageField(upload_to='student_id_card_photos_student/', blank=True, null=True)
    department = models.CharField(max_length=50)
    level = models.CharField(max_length=50)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    national_id_number = models.CharField(max_length=14)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    # profile_photo = models.ImageField(upload_to='profile_photos_student/', null=True, blank=True)
    department = models.CharField(max_length=100)
    admin_type = models.CharField(max_length=50)



# select * from accounts_student; select * from accounts_registration_request;
    
    