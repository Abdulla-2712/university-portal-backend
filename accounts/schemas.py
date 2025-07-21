from ninja import ModelSchema
from .models import Student

class studentSchema(ModelSchema):
    class Meta:
         model = Student
         fields = ['email','password']
