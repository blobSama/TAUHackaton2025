from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import requests
import os
import latex_analyser

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./exercises.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
scope = ""
    

# DB model
class ItemDB(Base):
    __tablename__ = "exercises"
    ex_num = Column(Integer, primary_key=True, index=True)
    question_num = Column(String, index=True)
    question = Column(String, index=True)
    answer = Column(String, index=True)
    scope = Column(String, index=True)

# Create the DB
Base.metadata.create_all(bind=engine)

# Pydantic model for input/output
class Item(BaseModel):
    ex_num: str
    question_num: str
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
        
# Items for the DB demo
item1 = ItemDB(ex_num=1, question_num="1", 
               question="""
                Prove the following statement:
                If a + 1/a is an integer, then a^3 + 1/a^3 is also an integer.
               """, 
               answer="""
                Step 1: § PROOF: [other]
                Step 2: Let a ∈ℤ [assumption]
                Step 3: Assume that: a + 1/a = b, where b ∈ℤ [assumption]
                Step 4: We want to show that a^3 + 1/a^3∈ℤ [other]
                Step 5: We use the identity: ( a + 1/a)^3 = a^3 + 1/a^3 + 3a ·1/a( a + 1/a) [other]
                Step 6: Since a ·1/a = 1, we simplify: ( a + 1/a)^3 = a^3 + 1/a^3 + 3 ( a + 1/a) [other]
                Step 7: Substitute b into the expression: b^3 = a^3 + 1/a^3 + 3b [other]
                Step 8: Rearrange to isolate a^3 + 1/a^3: a^3 + 1/a^3 = b^3 - 3b [inference]
                Step 9: Since b ∈ℤ, then b^3 - 3b ∈ℤ, and hence: a^3 + 1/a^3∈ℤ [inference]
                Step 10: § CONCLUSION: [other]
                Step 11: If a + 1/a is an integer, then a^3 + 1/a^3 is also an integer [inference]
               """, 
               scope=None)
item2 = ItemDB(ex_num=1, question_num="2", 
               question="""
                Prove the following inequality, 
                and find a necessary and sufficient condition for equality to hold:
                |a + 1/a| ≥ 2
               """, 
               answer="""
                Step 1: § PART 2 [other]
                Step 2: Let a ∈ℝ, with a ≠ 0 [assumption]
                Step 3: Then: [inference]
                Step 4: |a + 1/a| = |a| + | 1/a| [other]
                Step 5: By the Arithmetic-Geometric Mean Inequality (AM-GM), we have: [other]
                Step 6: |a| + | 1/a|/2≥√( |a| ·| 1/a| ) = √(1) = 1 [other]
                Step 7: Multiplying both sides by 2: [other]
                Step 8: |a| + | 1/a| ≥ 2 [other]
                Step 9: Equality holds if and only if: [case]
                Step 10: |a| = | 1/a| ⇒ a = ± 1 [other]
               """, 
               scope=None)
item3 = ItemDB(ex_num=1, question_num="3", 
               question="""
                Prove by induction:
                The sum from k = 1 to n (n ∈ ℕ) of k² = (1/6)n(2n+1)*(n+1)
               """, 
               answer="""
                Step 1: § PROOF BY INDUCTION [induction]
                Step 2: We aim to prove the following identity for all n ∈ℕ: [assumption]
                Step 3: ∑_k=1^n k^2 = 1/6n(n+1)(2n+1) [other]
                Step 4: Base case: [induction]
                Step 5: n = 1 [other]
                Step 6: ∑_k=1^1 k^2 = 1^2 = 1 1/6· 1 · (1+1) · (2 · 1 + 1) = 1/6· 1 · 2 · 3 = 1 [other]
                Step 7: Thus, the formula holds for n = 1 [inference]
                Step 8: Inductive step: [induction]
                Step 9: Assume the formula holds for some n = m ∈ℕ: [assumption]
                Step 10: ∑_k=1^m k^2 = 1/6m(m+1)(2m+1) [other]
                Step 11: We want to show that the formula holds for n = m+1, i [other]
                Step 12: e [other]
                Step 13: , [other]
                Step 14: ∑_k=1^m+1 k^2 = 1/6(m+1)(m+2)(2m+3) [other]
                Step 15: Start from the inductive hypothesis: [induction]
                Step 16: ∑_k=1^m+1 k^2 = ∑_k=1^m k^2 + (m+1)^2 = 1/6m(m+1)(2m+1) + (m+1)^2 [other]
                Step 17: Factor out (m+1): [other]
                Step 18: = (m+1) [ 1/6m(2m+1) + (m+1) ] [other]
                Step 19: = (m+1) [ 1/6m(2m+1) + 6(m+1)/6] [other]
                Step 20: = (m+1) [ 1/6( m(2m+1) + 6(m+1) ) ] [other]
                Step 21: = 1/6(m+1) ( 2m^2 + m + 6m + 6 ) = 1/6(m+1)(2m^2 + 7m + 6) [other]
                Step 22: Factor the quadratic: [other]
                Step 23: 2m^2 + 7m + 6 = (m+2)(2m+3) [other]
                Step 24: ⇒∑_k=1^m+1 k^2 = 1/6(m+1)(m+2)(2m+3) [other]
                Step 25: Thus, the formula holds for m+1, completing the inductive step [inference]
                Step 26: Conclusion: [other]
                Step 27: By mathematical induction, the identity ∑_k=1^n k^2 = 1/6n(n+1)(2n+1) holds for all n ∈ℕ [assumption]
               """, 
               scope=None)
item4 = ItemDB(ex_num=1, question_num="4", 
               question="""
                Prove that for any n ∈ ℕ:
                The sum from k = 0 to n of (-1)^k * (n choose k) = 0
               """, 
               answer="""
                Step 1: § PROOF [other]
                Step 2: We aim to prove that for every n ∈ℕ, n ≥ 1, [other]
                Step 3: ∑_k=0^n (-1)^k nk = 0 [other]
                Step 4: Proof using the Binomial Theorem: [other]
                Step 5: Recall the Binomial Theorem: [other]
                Step 6: (1 + x)^n = ∑_k=0^nnk x^k [other]
                Step 7: Substitute x = -1 into the identity: [other]
                Step 8: (1 + (-1))^n = ∑_k=0^nnk (-1)^k [other]
                Step 9: 0^n = ∑_k=0^n (-1)^k nk [other]
                Step 10: Since n ≥ 1, we have 0^n = 0 [other]
                Step 11: Therefore, [conclusion]
                Step 12: ∑_k=0^n (-1)^k nk = 0 [other]
                Step 13: Conclusion: [other]
                Step 14: ∑_k=0^n (-1)^k nk = 0 for all n ∈ℕ, n ≥ 1 [assumption]
               """, 
               scope=None)


# Routes

@app.get("/prompt")
def get_exercises(item: Item, db: Session = Depends(get_db)):
    # Get the scope from the file
    with open("scope.txt", "r") as file:
        scope = file.read()
    
    if scope == "":
        raise HTTPException(status_code=418, detail="Couldn't get the scope, code is as useful as a chocolate teapot.")
    
    add_exercise(item1)
    add_exercise(item2)
    add_exercise(item3)
    add_exercise(item4)
    
    # Get the exercise from the DB
    exercise = db.query(ItemDB).filter(ItemDB.ex_num == int(item.ex_num) 
                                       and ItemDB.question_num == int(item.question_num))
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    question = exercise.question
    model_answer = exercise.answer
    student_answer = latex_analyser.analyse_proof(item.answer + "\n$0")
    flag = item.command
    
    prompt_txt = ""
    
    # Get the prompt from the function
    if flag == "compare":
        prompt_txt = compare_answers_txt(model_answer, student_answer, scope)
    elif flag == "direction":
        prompt_txt = get_direction_txt(model_answer, student_answer, scope)
    elif flag == "hint":
        prompt_txt = get_hint_txt(model_answer, student_answer, scope)
    else:
        raise HTTPException(status_code=400, detail="Invalid command")
    
    # Send the prompt to the API
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        headers={"Content-Type": "application/json"},
        params={"key": AIzaSyBAnRfmMZr7l18uW5UJJ3EV_P6-VwKlPws},
        json={
            "contents": [
                {
                    "parts": [{"text": prompt_txt}],
                    "role": "user"
                }
            ]
        }
    )
    
    # Get the output from the API, and return it
    gemini_output = response.json()
    print(gemini_output)
    return gemini_output["candidates"][0]["content"][0]["parts"][0]["text"]
    

def compare_answers_txt(model_answer: str, student_answer: str, scope: str):
    prompt = f"""
    You are an expert calculus tutor reviewing a student's solution to a calculus exercise. You will be given:
    - The official solution (called "Official Solution").
    - A student's solution (called "Student Solution").
    - A scope of knowledge that defines what is permitted for evaluating correctness (called "Scope").

    Your task is to:
    1. Analyze and deconstruct both solutions.
    2. Compare the Student Solution to the Official Solution, focusing on **correctness**, **rigor**, and adherence to the **Scope**.
    3. If the student uses methods or facts **outside of the provided Scope**, clearly state: **"I cannot verify this answer as it uses information out of my scope."**
    4. If the student’s answer is incorrect or less rigorous than the official one, explain why.
    5. If the student's solution is correct and rigorous within the Scope, confirm its correctness.

    Return a clear and detailed evaluation.

    Official Solution:
    {model_answer}

    Student Solution:
    {student_answer}

    Scope:
    {scope}

    """
    return prompt

def get_direction_txt(model_answer: str, student_answer: str, scope: str):
    prompt = f"""
    You are an expert calculus tutor evaluating the direction a student is taking to solve a problem. You will be given:
    - The official solution (called "Official Solution").
    - A student's partial or complete attempt (called "Student Solution").
    - A scope of knowledge (called "Scope").

    Your task is to:
    1. Analyze and deconstruct the logical flow and method used in both the Official and Student Solutions.
    2. Determine whether the **Student Solution is progressing in the same general direction** as the Official Solution.
    3. If the direction differs and relies on concepts not in the Scope, you must say: **"The direction is dissimilar, and I cannot verify this direction as it uses information out of my scope."**
    4. If the direction is similar and within the Scope, confirm this and briefly explain how.

    Your answer should be clear and instructive.

    Official Solution:
    {model_answer}

    Student Solution:
    {student_answer}

    Scope:
    {scope}

    """
    return prompt

def get_hint_txt(model_answer: str, student_answer: str, scope: str):
    prompt = f"""
    You are an expert calculus tutor providing hints to guide a student toward a correct solution. You will be given:
    - The official step-by-step solution (called "Official Solution").
    - A student's partial or empty solution (called "Student Solution").
    - A scope of permitted knowledge (called "Scope").

    Your task is to:
    1. Identify the furthest step in the Student Solution that **matches a step in the Official Solution**.
    2. If the Student Solution contains information not found in the Official Solution and outside the Scope, disregard those steps.
    3. From the last matching valid step (or from the beginning if there’s no match), give a clear and rigorous **hint** to help the student proceed toward the correct answer.
    4. **State clearly from which step your hint is continuing.**

    If no valid progress can be verified due to out-of-scope content, say:
    **"I cannot verify the student's solution as it uses information out of my scope. I will provide a hint starting from the beginning."**

    Official Solution:
    {model_answer}

    Student Solution:
    {student_answer}

    Scope:
    {scope}

    """
    return prompt

def add_exercise(exercise: ItemDB, db: Session = Depends(get_db)):
    db_item = ItemDB(ex_num=exercise.ex_num, question_num=exercise.question_num, question=exercise.question, answer=exercise.answer, scope=exercise.scope)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item