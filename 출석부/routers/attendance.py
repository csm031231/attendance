from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from base import get_db
from model import Attendance, Student
from dto import AttendanceCreateDTO, AttendanceResponseDTO
from typing import List

router = APIRouter(prefix="/attendance", tags=["출석"])

# 출석 등록
@router.post("/", response_model=AttendanceResponseDTO)
def create_attendance(attendance_data: AttendanceCreateDTO, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == attendance_data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")

    existing = db.query(Attendance).filter(
        Attendance.student_id == attendance_data.student_id,
        Attendance.date == attendance_data.date
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 해당 날짜의 출석 기록이 존재합니다.")

    attendance = Attendance(**attendance_data.dict())
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

# 특정 날짜의 전체 출석 조회
@router.get("/", response_model=List[AttendanceResponseDTO])
def get_attendance_by_date(date: str = Query(...), db: Session = Depends(get_db)):
    records = db.query(Attendance).filter(Attendance.date == date).all()
    return records

# 특정 학생의 전체 출석 조회
@router.get("/student/{student_id}", response_model=List[AttendanceResponseDTO])
def get_attendance_for_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")

    records = db.query(Attendance).filter(Attendance.student_id == student_id).all()
    return records
