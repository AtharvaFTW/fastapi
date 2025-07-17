from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from utils import db

router=APIRouter()

class ReferenceText(BaseModel):
    topic_id:int
    reference_text:str

class TopicRef(BaseModel):
    id:int
    name:str

class SubjectRef(BaseModel):
    id:int
    name:str

class CourseRef(BaseModel):
    id:int
    name:str

@router.get("/courses", response_model=List[CourseRef])
def get_courses():
    courses = db.fetch_courses()
    return [CourseRef(id=row[0], name=row[1]) for row in courses]

@router.get("/subjects/{course_id}", response_model=List[SubjectRef])
def get_subjects(course_id: int):
    subjects = db.fetch_subjects(course_id)
    return [SubjectRef(id=row[0], name=row[1]) for row in subjects]

@router.get("/topics/{subject_id}", response_model=List[TopicRef])
def get_topics(subject_id: int):
    topics = db.fetch_topics(subject_id)
    return [TopicRef(id=row[0], name=row[1]) for row in topics]

@router.get("/reference/{topic_id}", response_model=ReferenceText)
def get_reference_text(topic_id: int):
    with db.get_connection() as conn:
        row = conn.execute("SELECT reference_text FROM topic_content WHERE topic_id = ?", (topic_id,)).fetchone()
    if row and row[0]:
        return ReferenceText(topic_id=topic_id, reference_text=row[0])
    raise HTTPException(status_code=404, detail="Reference text not found")

@router.post("/reference", response_model=ReferenceText)
def save_reference_text(ref: ReferenceText):
    with db.get_connection() as conn:
        conn.execute("""
            INSERT INTO topic_content (topic_id, reference_text)
            VALUES (?, ?)
            ON CONFLICT(topic_id) DO UPDATE SET reference_text = excluded.reference_text, updated_at = CURRENT_TIMESTAMP
        """, (ref.topic_id, ref.reference_text.strip()))
        conn.commit()
    return ref