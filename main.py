from fastapi import FastAPI,Depends
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from models import Todos
from database import engine,SessionLocal


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@app.get("/")
async def read_all(db:db_dependency):
    return db.query(Todos).all()


