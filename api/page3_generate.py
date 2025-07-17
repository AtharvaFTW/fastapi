from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from utils import db
from utils.openai_content import generate_content

router = APIRouter()

# ---------- Models ----------
class ContentRequest(BaseModel):
    topic_id: int
    reference_text: str

class ContentResponse(BaseModel):
    content_text: str
    image_urls: List[str]

# ---------- Endpoints ----------

@router.post("/generate", response_model=ContentResponse)
def generate_and_save_content(req: ContentRequest):
    if not req.reference_text.strip():
        raise HTTPException(status_code=400, detail="Reference text is empty.")

    sanitized_topic = f"topic_{req.topic_id}"
    content_text, img_urls = generate_content(req.reference_text, sanitized_topic=sanitized_topic)

    with db.get_connection() as conn:
        conn.execute("""
            INSERT INTO topic_content (topic_id, content_text, image_urls, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(topic_id) DO UPDATE SET
                content_text=excluded.content_text,
                image_urls=excluded.image_urls,
                updated_at=CURRENT_TIMESTAMP
        """, (req.topic_id, content_text, ",".join(img_urls)))
        conn.commit()

    return ContentResponse(content_text=content_text, image_urls=img_urls)
