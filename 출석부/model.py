from sqlalchemy import Column, Integer, String, ForeignKey, Date
from base import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    students_number = Column(String, unique=True, nullable=False)

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)  # YYYY-MM-DD 형식
    status = Column(String, nullable=False)  # present / absent
