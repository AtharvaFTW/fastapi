from fastapi import FastAPI,HTTPException,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from api import page1_data,page2_reference,page3_generate,page4_slide_deck

app=FastAPI()
@app.route("/")
def root():
    return {"message":"hello"}

app.include_router(page1_data.router,prefix="/api/data", tags=["Page 1 -Data"])
app.include_router(page2_reference.router, prefix="/api/reference", tags=["Page 2 - Reference Text"])
app.include_router(page3_generate.router, prefix="/api/generate", tags=["Page 3 - Generate Content"])
app.include_router(page4_slide_deck.router, prefix="/api/slides", tags=["Page 4 - Slides"])

