from ninja import Schema, Router
from ninja.errors import HttpError
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth  # If you're using Ninja JWT
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime, timedelta
import jwt

from compsuggs.models import Complaint
from accounts.models import Student  # Import the Student model

router = Router()


class ComplaintSchema(Schema):
    department: str
    subject: str
    priority_level: str
    complaint_content: str
    student: int

class fullComplaintSchema(Schema):
    department: str
    subject: str
    priority_level: str
    complaint_content: str
    complaint_answer: str
    status: str
    student: int


@router.post("/submit_complaint")
def submit_complaint(request, data: ComplaintSchema):
    try:
        student_instance = get_object_or_404(Student, id=data.student)
        complaint = Complaint.objects.create(
            department=data.department,
            subject=data.subject,
            priority_level=data.priority_level,
            complaint_content=data.complaint_content,
            student=student_instance, 

        )
        return {"message": "Complaint saved successfully", "complaint_id": complaint.id}
    except Student.DoesNotExist:
        raise HttpError(404, "Student not found")
    except Exception as e:
        print(f"Error creating complaint: {str(e)}")  # Debug log
        raise HttpError(400, f"Failed to save request: {str(e)}")



@router.get('/get_all_comps')
def get_all_comps(request):
    # Get the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'No valid token provided'}, status=401)
    
    token = auth_header.split(' ')[1]
    
    try:
        # Decode the JWT token
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        student_id = decoded_token.get('id')
        
        if not student_id:
            return JsonResponse({'error': 'Invalid token: no student ID found'}, status=401)
        
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token has expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=401)
    
    # Filter complaints by student_id
    comps = Complaint.objects.filter(student_id=student_id)
    
    data = [
        {
            "id": req.id,
            "department": req.department,
            "subject": req.subject,
            "priority_level": req.priority_level,
            "complaint_content": req.complaint_content,
            "complaint_answer": req.complaint_answer,
            "status": req.status
        }
        for req in comps
    ]
    
    return JsonResponse(data, safe=False)


