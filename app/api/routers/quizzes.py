from fastapi import APIRouter, Depends, HTTPException
from requests import Session

from app.db import quiz_crud, text_crud, schemas
from app.db.database import SessionLocal, TextsSessionLocal
from app.service.quiz_generator.common import Quiz, QuizBuilder
from app.service.quiz_generator.generator import QuizGenerator

router = APIRouter(
    prefix="/api/quizzes",
    tags=["quizzes"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_data_db():
    db_texts = TextsSessionLocal()
    try:
        yield db_texts
    finally:
        db_texts.close()


@router.get("/")
async def get_quiz_batch(simple: int = 10, voice: int = None, sequence: int = None, context: int = None, db: Session = Depends(get_db)):
    return {"message": "get batch of different quizzes"}


@router.get("/simple", response_model=list[schemas.SimpleQuiz])
async def get_simple_quiz_batch(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_quizzes = quiz_crud.get_simple_quizzes(db=db, skip=offset, limit=limit)
    return db_quizzes


@router.post("/simple", response_model=schemas.SimpleQuiz)
def create_simple_quiz(quiz: schemas.SimpleQuizCreate, answers: list[schemas.SimpleAnswerCreate], db: Session = Depends(get_db)):
    db_quiz = quiz_crud.get_simple_quiz_by_text(db, text=quiz.text)
    if db_quiz:
        raise HTTPException(status_code=400, detail="Quiz already exists")
    return quiz_crud.create_complete_simple_quiz(db=db, quiz=quiz, answers=answers)


@router.post("/simple/auto")
def create_simple_quiz(limit: int = 10, quiz_db: Session = Depends(get_db), data_db: Session = Depends(get_data_db)):
    db_dataset = text_crud.get_dataset_by_title(
        data_db, title="alice-s-adventures-in-wonderland.txt")
    if not db_dataset:
        return {"message": "dataset not found"}

    try:
        generator = QuizGenerator(QuizBuilder())
        quizzes: list[Quiz] = []
        l = 0
        for feature in db_dataset.entries:
            if (l > limit):
                break
            q = generator.generate_single_grammar(
                source=feature.text, number_or_answers=4)
            if q.is_valid():
                quizzes.append(q)
                l += 1
        
        for q in quizzes:
            if quiz_crud.get_simple_quiz_by_text(db=quiz_db, text=q.text):
                continue
            quiz_create, answers_create = q.to_create_schema()
            quiz_crud.create_complete_simple_quiz(db=quiz_db, quiz=quiz_create, answers=answers_create)
        
        return {"quizzes": quizzes}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"encountered error {e}")


@router.get("/voice")
async def get_voice_quiz():
    return {"message": "generate voice quiz"}


@router.get("/sequence")
async def get_sequence_quiz():
    return {"message": "generate sequence quiz"}


@router.get("/context")
async def get_context_quiz():
    return {"message": "generate context quiz"}
