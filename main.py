from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def readroot():
    return {"Hello":"World"}