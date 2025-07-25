
# Register your models here.
# accounts/admin.py
from django.contrib import admin
from .models import Student
from .models import Registration_Request
from .models import Admin

admin.site.register(Student)
admin.site.register(Registration_Request)
admin.site.register(Admin)
