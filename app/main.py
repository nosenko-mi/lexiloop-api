from fastapi import Depends, FastAPI

from app.api.routers import data, quizzes
from app.db import models
from app.db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(quizzes.router)
app.include_router(data.router)

@app.get("/")
async def root():
    return {"message": "Simple quiz generator, inspired by Duolingo. Uses public domain data to create quizzes."}


# how to run:
# *D:\dev\quiz_generator>* uvicorn app.main:app --reload