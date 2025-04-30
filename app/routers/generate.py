# app/routers/generate.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth import get_current_user
from app.utils.deepai import generate_text
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate")
def generate_from_prompt(req: PromptRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.credits < 1:
        raise HTTPException(status_code=402, detail="Not enough credits")

    text = generate_text(req.prompt)

    if not text:
        raise HTTPException(status_code=500, detail="AI failed to generate text")

    # Deduct credit
    user.credits -= 1
    db.add(user)
    db.commit()

    return {"result": text, "remaining_credits": user.credits}
