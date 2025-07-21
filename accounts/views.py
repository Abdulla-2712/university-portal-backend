from .models import Student
from .schemas import studentSchema

def loginStudent(data: studentSchema):
    try:
        student = Student.objects.get(email=data.email, password=data.password)
        return {"message": "Login successful"}
    except Student.DoesNotExist:
        return {"error": "Invalid email or password"}
