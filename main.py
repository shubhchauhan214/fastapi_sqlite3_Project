from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import models
from models import Students
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# Read all contents
@app.get("/")
async def students(db: db_dependency):
    return db.query(Students).all()


# # Get content using id
# @app.get("/student/{student_id}")
# async def student_by_id(db:db_dependency, student_id: int):
#     student_model = db.query(School).filter(School.id == )