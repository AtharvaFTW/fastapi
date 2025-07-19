from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import db
from typing import List, Optional

router = APIRouter()

class Course(BaseModel):
    id: Optional[int] = None
    name: str

class Subject(BaseModel):
    id: Optional[int] = None
    course_id: int
    name: str

class Topic(BaseModel):
    id: Optional[int] = None
    subject_id: int
    name: str

@router.get("/courses", response_model=List[Course])
def get_courses():
    rows = db.fetch_courses()
    return [{"id": row[0], "name": row[1]} for row in rows]

@router.post("/courses", response_model=Course)
def add_course(course: Course):
    with db.get_connection() as conn:
        conn.execute("INSERT INTO courses (name) VALUES (?)", (course.name,))
        conn.commit()
        course_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    return {**course.dict(), "id": course_id}

@router.get("/subjects/{course_id}", response_model=List[Subject])
def get_subjects(course_id: int):
    rows = db.fetch_subjects(course_id)
    return [{"id": row[0], "course_id": course_id, "name": row[1]} for row in rows]

@router.post("/subjects", response_model=Subject)
def add_subject(subject: Subject):
    with db.get_connection() as conn:
        conn.execute("INSERT INTO subjects (course_id, name) VALUES (?, ?)", (subject.course_id, subject.name))
        conn.commit()
        subject_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    return {**subject.dict(), "id": subject_id}

@router.get("/topics/{subject_id}", response_model=List[Topic])
def get_topics(subject_id: int):
    rows = db.fetch_topics(subject_id)
    return [{"id": row[0], "subject_id": subject_id, "name": row[1]} for row in rows]

@router.post("/topics", response_model=Topic)
def add_topic(topic: Topic):
    with db.get_connection() as conn:
        conn.execute("INSERT INTO topics (subject_id, name) VALUES (?, ?)", (topic.subject_id, topic.name))
        conn.commit()
        topic_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    return {**topic.dict(), "id": topic_id}
