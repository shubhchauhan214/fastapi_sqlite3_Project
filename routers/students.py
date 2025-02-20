from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path

from models import Students
from database import SessionLocal
from starlette import status


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class StudentRequest(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    address: str = Field(min_length=3)


# Read all contents
@router.get("/", status_code=status.HTTP_200_OK)
async def students(db: db_dependency):
    return db.query(Students).all()


# Read content using id
@router.get("/student/{student_id}", status_code=status.HTTP_200_OK)
async def student_by_id(db:db_dependency, student_id: int = Path(gt=0)):
    student_model = db.query(Students).filter(Students.id == student_id).first()
    if student_model is not None:
        return student_model
    raise HTTPException(status_code=404, detail='Student not found.')


# POST Request Method
@router.post("/student", status_code=status.HTTP_201_CREATED)
async def new_student(db: db_dependency, student_request: StudentRequest):
    student_model = Students(**student_request.dict())

    db.add(student_model)
    db.commit()


# PUT Request Method
@router.put("/student/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(db: db_dependency,
                         student_request: StudentRequest,
                         student_id: int = Path(gt=0)):
    student_model = db.query(Students).filter(Students.id == student_id).first()
    if student_model is None:
        raise HTTPException(status_code=404, detail='Student not found')

    student_model.first_name = student_request.first_name
    student_model.last_name = student_request.last_name
    student_model.address = student_request.address

    db.add(student_model)
    db.commit()


# DELETE Method
@router.delete("/student/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(db: db_dependency, student_id: int = Path(gt=0)):
    student_model = db.query(Students).filter(Students.id == student_id).first()
    if student_model is None:
        raise HTTPException(status_code=404, detail='Student not found')
    db.query(Students).filter(Students.id == student_id).delete()

    db.commit()



