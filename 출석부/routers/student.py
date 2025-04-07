from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from base import get_db
from model import Student
from dto import StudentCreateDTO, StudentUpdateDTO, StudentResponseDTO
from typing import List

router = APIRouter(prefix="/students", tags=["학생"])

# 학생 등록
@router.post("", response_model=StudentResponseDTO)
def create_student(student_data: StudentCreateDTO, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.students_number == student_data.students_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 등록된 학번입니다.")
    
    student = Student(**student_data.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

# 학생 전체 조회
@router.get("/", response_model=List[StudentResponseDTO])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

# 학생 정보 수정
@router.put("/{student_id}/change", response_model=StudentResponseDTO)
def update_student(student_id: int, student_data: StudentUpdateDTO, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    
    for key, value in student_data.dict().items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student

# 학생 삭제
@router.delete("/{student_id}/del", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    
    db.delete(student)
    db.commit()
