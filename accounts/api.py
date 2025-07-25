# accounts/api.py

from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from django.shortcuts import get_object_or_404
from ninja import Schema, Router
from ninja.errors import HttpError
from django.conf import settings
from datetime import datetime, timedelta
import jwt
from accounts.models import Student, Registration_Request, Admin
from .auth import JWTAuth
from compsuggs.api import router as compsuggs_router  # Import compsuggs router

router = Router()
api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)  # JWT controller
api.add_router("/compsuggs/", compsuggs_router)
api.add_router("/", router)  # ← ✅ Add this line to register the `router`


auth = JWTAuth()
SECRET_KEY = settings.SECRET_KEY

class UserLoginSchema(Schema):
    email: str
    password: str
class AdminLoginSchema(Schema):
    email: str
    password:str
class UserRequestSchema(Schema):
    name: str
    email: str
    phone_number: str
    Seat_Number: str
    level: str
    department: str
class AddStudentSchema(Schema):
    name: str
    email: str
    phone_number: str
    Seat_Number: str
    level: str
    department: str   

@api.post("/login_student")
def Slogin(request, data: UserLoginSchema):
    try:
        student = Student.objects.get(email = data.email)
        if student.password == data.password:
            payload = {
                "id": student.id,
                "email": student.email,
                "exp": datetime.utcnow() + timedelta(minutes=60)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return {"token": token, "message": "Login successful"}
        else:
            raise HttpError(401, "Invalid password")
    except Student.DoesNotExist:
        raise HttpError(404, "User not found")

@api.post("/login_admin")
def Alogin(request, data: AdminLoginSchema):
    try:
        admin = Admin.objects.get(email = data.email)
        if admin.password == data.password:
            payload = {
                "id": admin.id,
                "email": admin.email,
                "exp": datetime.utcnow() + timedelta(minutes=60)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return {"token": token, "message": "Login successful"}
        else:
            raise HttpError(401, "Invalid password")
    except Admin.DoesNotExist:
        raise HttpError(404, "User not found")



@router.post("/submit_request")
def submit_request(request, data: UserRequestSchema):
    if Student.objects.filter(email=data.email).exists():
        raise HttpError(409, "A student with this email already exists.")
    if Student.objects.filter(Seat_Number= data.Seat_Number).exists():
        raise HttpError(409, "A student with this Seat number already exists.")
    try:
        Registration_Request.objects.create(
            name=data.name,
            email=data.email,
            phone_number=data.phone_number,
            Seat_Number=data.Seat_Number,
            level=data.level,
            department=data.department
        )
        return {"message": "Request saved successfully"}
    except Exception as e:
        raise HttpError(400, f"Failed to save request: {str(e)}")


@api.get("/get_all_requests")
def get_all_requests(request):
    requests = Registration_Request.objects.all()
    data = [
        {
            "id": req.id,
            "FullName": req.name,
            "PhoneNumber": req.phone_number,
            "AcademicEmail": req.email,
            "SeatNumber": req.Seat_Number,
            "Level": req.level,
            "Department": req.department
        }
        for req in requests
    ]
    return data

@router.post("/add_user")
def add_user(request, data: UserRequestSchema):
    if Student.objects.filter(email=data.email).exists():
        raise HttpError(409, "A student with this email already exists.")
    if Student.objects.filter(Seat_Number= data.Seat_Number).exists():
        raise HttpError(409, "A student with this Seat number already exists.")
    try:
        Student.objects.create(
            name=data.name,
            email=data.email,
            phone_number=data.phone_number,
            Seat_Number=data.Seat_Number,
            level=data.level,
            department=data.department
        )
        return {"message": "Request saved successfully"}
    except Exception as e:
        raise HttpError(400, f"Failed to save request: {str(e)}")


@router.delete("/delete_request/{request_id}")
def delete_request(request, request_id: int):
    obj = get_object_or_404(Registration_Request, id=request_id)
    obj.delete()
    return {"message": "Request deleted successfully"}
