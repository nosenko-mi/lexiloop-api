from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    source = Column(String)

    entries = relationship("TextFeature", back_populates="dataset")


class TextFeature(Base):
    __tablename__ = "text_features"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))

    dataset = relationship("Dataset", back_populates="entries")


class QuizType(Base):
    __tablename__ = "quiz_type"

    id = Column(Integer, primary_key=True)
    type_text = Column(String)


class SimpleQuiz(Base):
    __tablename__ = "simple_quizzes"

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey("quiz_type.id"))
    text = Column(String)

    answers = relationship("SimpleAnswer", back_populates="quiz")


class SequenceQuiz(Base):
    __tablename__ = "sequence_quizzes"

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey("quiz_type.id"))
    text = Column(String)

    answers = relationship("SequenceAnswer", back_populates="quiz")


class VoiceQuiz(Base):
    __tablename__ = "voice_quizzes"

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey("quiz_type.id"))
    text = Column(String)
    expected_text = Column(String)


class SimpleAnswer(Base):
    __tablename__ = "simple_answers"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_correct = Column(String)
    quiz_id = Column(Integer, ForeignKey("simple_quizzes.id"))

    quiz = relationship("SimpleQuiz", back_populates="answers")


class SequenceAnswer(Base):
    __tablename__ = "sequence_answers"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    position = Column(Integer)
    quiz_id = Column(Integer, ForeignKey("sequence_quizzes.id"))

    quiz = relationship("SequenceQuiz", back_populates="answers")
