from ninja import NinjaAPI
from .views import loginStudent
from .schemas import studentSchema

api = NinjaAPI()

@api.post("/loginStudent")
def login_student_api(request, data: studentSchema):
    return loginStudent(data)
