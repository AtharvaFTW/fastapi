from fastapi import FastAPI
import db

app=FastAPI()
@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/api/courses")
def get_all_courses():
    courses=db.fetch_courses()
    return {"Courses": courses}