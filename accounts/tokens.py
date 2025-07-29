import secrets
from datetime import datetime, timedelta
from accounts.models import Student, Registration_Request, Admin
from django.utils import timezone


def generate_reset_token():
    return secrets.token_urlsafe(32)

def create_password_reset_token(user):
    token = generate_reset_token()
    user.password_reset_token = token
    user.reset_token_created_at = datetime.now()
    user.save()
    return token

def verify_token(token: str):
    try:
        user = Student.objects.get(password_reset_token=token)
    except Student.DoesNotExist:
        return None
    
    if user.reset_token_created_at is None:
        return None
    
    expiration_time = user.reset_token_created_at + timedelta(minutes = 30)
    now_time = timezone.now()
    if now_time > expiration_time:
        return None
    
    return user