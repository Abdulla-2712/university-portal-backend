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
from django.core.mail import send_mail
from django.conf import settings

from compsuggs.models import Complaint, Suggestion
from accounts.models import Student  # Import the Student model

router = Router()
class SuggestionStatSchema(Schema):
    id: int
    status: str
class SuggestionStatAnswerSchema(Schema):
    id: int
    suggestion_answer: str
    status: str

class ComplaintStatSchema(Schema):
    id: int
    status: str
class ComplaintStatAnswerSchema(Schema):
    id: int
    complaint_answer: str
    status: str

class ComplaintSchema(Schema):
    department: str
    subject: str
    priority_level: str
    complaint_content: str
    student: int
class SuggestionSchema(Schema):
    department: str
    subject: str
    suggestion_content: str
    student: int




@router.get('/get_all_suggs')
def get_all_suggs(request):
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
    suggs = Suggestion.objects.filter(student_id=student_id)
    
    data = [
        {
            "id": req.id,
            "department": req.department,
            "subject": req.subject,
            "complaint_content": req.complaint_content,
            "complaint_answer": req.complaint_answer,
            "status": req.status
        }
        for req in suggs
    ]
    
    return JsonResponse(data, safe=False)


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


@router.post("/submit_suggestion")
def submit_suggestion(request, data: SuggestionSchema):
    try:
        student_instance = get_object_or_404(Student, id = data.student)
        suggestions = Suggestion.objects.create(
            department = data.department,
            subject=data.subject,
            suggestion_content=data.suggestion_content,
            student=student_instance, 
        )
        return {"message": "Complaint saved successfully", "complaint_id": suggestions.id}
    except Student.DoesNotExist:
        raise HttpError(404, "Student not found")
    except Exception as e:
        print(f"Error creating complaint: {str(e)}")  # Debug log
        raise HttpError(400, f"Failed to save request: {str(e)}")

@router.get('/get_user_compsuggs')
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

    comps = Complaint.objects.filter(student_id=student_id)
    suggs = Suggestion.objects.filter(student_id=student_id)
    datac = [
        {
            "id": f"comp-{req.id}",
            "department": req.department,
            "subject": req.subject,
            "priority_level": req.priority_level,
            "content": req.complaint_content,
            "answer": req.complaint_answer,
            "status": req.status
        }
        for req in comps
    ]
    datas = [
        {
            "id": f"sugg-{req.id}",
            "department": req.department,
            "subject": req.subject,
            "priority_level": None,  # Added to match the schema
            "content": req.suggestion_content,
            "answer": req.suggestion_answer,
            "status": req.status
        }
        for req in suggs
    ]
    combined = datac + datas
    return JsonResponse(combined, safe=False)



@router.get('/get_admin_suggs')
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
    
    suggs = Suggestion.objects.all()
    data = [
        {
            "id": req.id,
            "department": req.department,
            "subject": req.subject,
            "priority_level": None,  # Added to match the schema
            "suggestion_content": req.suggestion_content,
            "suggestion_answer": req.suggestion_answer,
            "status": req.status
        }
        for req in suggs
    ]
    return JsonResponse(data, safe=False)


@router.post("/change_status_sugs")
def change_status(request, data: SuggestionStatSchema):

    sugg = Suggestion.objects.get(id=data.id)

    try:
        sugg.status = data.status
        sugg.save()
        return {"message": "status changed successfully"}
    except Student.DoesNotExist:
        raise HttpError(404, "complaint not found")

@router.post("/answer_suggestion")
def change_status(request, data: SuggestionStatAnswerSchema):
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

    sugg = Suggestion.objects.get(id=data.id)

    try:
        sugg.status = data.status
        sugg.suggestion_answer = data.suggestion_answer
        sugg.save()
        subject = 'Your suggestion has been answered..'
        message = f'Subject: {sugg.subject}\nSuggestion: {sugg.suggestion_content}\nAnswer: {sugg.suggestion_answer}'
        email_from = settings.EMAIL_HOST_USER
        return {"message": "status changed successfully"}
    except Student.DoesNotExist:
        raise HttpError(404, "complaint not found")










@router.get('/get_admin_comps')
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
    
    comps = Complaint.objects.all()
    data = [
        {
            "id": req.id,
            "department": req.department,
            "subject": req.subject,
            "priority_level": req.priority_level,  # Added to match the schema
            "complaint_content": req.complaint_content,
            "complaint_answer": req.complaint_answer,
            "status": req.status
        }
        for req in comps
    ]
    return JsonResponse(data, safe=False)


@router.post("/change_status_comp")
def change_status(request, data: ComplaintStatSchema):

    comp = Complaint.objects.get(id=data.id)

    try:
        comp.status = data.status
        comp.save()
        return {"message": "status changed successfully"}
    except Student.DoesNotExist:
        raise HttpError(404, "complaint not found")

@router.post("/answer_complaint")
def change_status(request, data: ComplaintStatAnswerSchema):
    comp = Complaint.objects.get(id=data.id)

    try:
        comp.status = data.status
        comp.complaint_answer = data.complaint_answer
        comp.save()
        return {"message": "status changed successfully"}
    except Student.DoesNotExist:
        raise HttpError(404, "complaint not found")