from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from utils import db
from utils.openai_slide import generate_slide_deck

router = APIRouter()

# ---------- Models ----------
class SlideRequest(BaseModel):
    topic_id: int
    overwrite: Optional[bool] = False

class SlideResponse(BaseModel):
    message: str
    slide_deck_md: Optional[str] = None

# ---------- Endpoints ----------

@router.post("/generate", response_model=SlideResponse)
def generate_slide(req: SlideRequest):
    topic_id = req.topic_id

    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT content_text, image_urls, slide_deck_md FROM topic_content WHERE topic_id = ?",
            (topic_id,)
        ).fetchone()

    if not row or not row[0] or not row[1]:
        raise HTTPException(status_code=400, detail="Please generate content and images for this topic first.")

    content_text = row[0]
    image_urls = [url.strip() for url in row[1].split(",") if url.strip()]
    slide_deck_exists = row[2] is not None and row[2].strip() != ""

    if slide_deck_exists and not req.overwrite:
        return SlideResponse(
            message="Slide deck already exists for this topic. Overwrite not allowed unless explicitly requested.",
            slide_deck_md=row[2]
        )

    slide_deck_md = generate_slide_deck(content_text, image_urls)

    with db.get_connection() as conn:
        conn.execute(
            """
            UPDATE topic_content
            SET slide_deck_md = ?, updated_at = CURRENT_TIMESTAMP
            WHERE topic_id = ?
            """,
            (slide_deck_md, topic_id)
        )
        conn.commit()

    return SlideResponse(message="Slide deck generated successfully.", slide_deck_md=slide_deck_md)


@router.get("/preview/{topic_id}", response_model=SlideResponse)
def get_slide_preview(topic_id: int):
    with db.get_connection() as conn:
        row = conn.execute(
            "SELECT slide_deck_md FROM topic_content WHERE topic_id = ?",
            (topic_id,)
        ).fetchone()

    if not row or not row[0]:
        raise HTTPException(status_code=404, detail="No slide deck found for this topic.")

    return SlideResponse(message="Slide deck found.", slide_deck_md=row[0])
