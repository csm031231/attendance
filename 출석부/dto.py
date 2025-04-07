from pydantic import BaseModel
from datetime import datetime

class StudentCreateDTO(BaseModel):
    name: str
    students_number: str

class StudentUpdateDTO(BaseModel):
    name: str
    students_number: str

class StudentResponseDTO(BaseModel):
    id: int
    name: str
    students_number: str

    class Config:
        orm_mode = True


class AttendanceCreateDTO(BaseModel):
    student_id: int
    date: datetime
    status: str  

class AttendanceResponseDTO(BaseModel):
    id: int
    student_id: int
    date: str
    status: str

    class Config:
        orm_mode = True
