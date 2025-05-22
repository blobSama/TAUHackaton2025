from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./exercises.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# DB model
class ItemDB(Base):
    __tablename__ = "exercises"
    exercise_id = Column(Integer, primary_key=True, index=True)
    question_num = Column(String, index=True)
    question = Column(String, index=True)
    answer = Column(String, index=True)

# Create the DB
Base.metadata.create_all(bind=engine)

# Pydantic model for input/output
class Item(BaseModel):
    exercise_id: str
    question_num: str
    question: str
    answer: str
    command: str

class ItemOut(Item):
    id: int
    class Config:
        orm_mode = True

# FastAPI app
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes

@app.get("/get_exercises")
def get_exercises(item: Item, db: Session = Depends(get_db)):
    exercise = db.query(ItemDB).filter(ItemDB.exercise_id == int(item.exercise_id)).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    question = exercise.question
    model_answer = exercise.answer
    student_answer = item.answer
    flag = item.command
    
    if flag == "compare":
        return compare_answers(model_answer, student_answer)
    elif flag == "direction":
        return get_direction(model_answer, student_answer)
    elif flag == "hint":
        return get_hint(model_answer, student_answer)
    else:
        raise HTTPException(status_code=400, detail="Invalid command")
    
    

def compare_answers(model_answer: str, student_answer: str):
    return None

def get_direction(model_answer: str, student_answer: str):
    return None

def get_hint(model_answer: str, student_answer: str):
    return None
