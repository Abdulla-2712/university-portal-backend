from django.db import models

# Create your models here.
# -------------------- شكاوي --------------------
class Complaint(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    priority_level = models.CharField(max_length=50)
    complaint_content = models.TextField()
    complaint_answer = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='complaints')
    admin = models.ForeignKey('accounts.Admin', on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_complaints')

# -------------------- اقتراحات --------------------
class Suggestion(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    suggestion_content = models.TextField()
    suggestion_answer = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='suggestions')
    admin = models.ForeignKey('accounts.Admin', on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_suggestions')
