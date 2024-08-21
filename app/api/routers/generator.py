from fastapi import APIRouter, Depends, HTTPException
from requests import Session


router = APIRouter(
    prefix="/api/admin",
    tags=["admin", "generator"]
)

@router.get("/source")
async def  get_quiz_batch():
    return {"message": f"possible sources for quizzes"}


@router.post("/batch")
async def  get_quiz_batch():
    return {"message": f"generate large batch from source"}