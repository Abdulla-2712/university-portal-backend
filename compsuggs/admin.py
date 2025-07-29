from django.contrib import admin
from .models import Complaint, Suggestion
# Register your models here.

admin.site.register(Complaint)
admin.site.register(Suggestion)