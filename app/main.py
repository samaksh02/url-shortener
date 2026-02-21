from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import hashlib

from .database import SessionLocal, engine
from .models import URL, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

class ShortenRequest(BaseModel):
    long_url: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_code(long_url: str) -> str:
    return hashlib.sha256(long_url.encode()).hexdigest()[:6]

@app.post("/shorten")
def shorten_url(request: ShortenRequest, db: Session = Depends(get_db)):
    short_code = generate_short_code(request.long_url)

    existing = db.query(URL).filter(URL.short_code == short_code).first()
    if not existing:
        url = URL(short_code=short_code, long_url=request.long_url)
        db.add(url)
        db.commit()

    return {
        "short_code": short_code,
        "long_url": request.long_url
    }

@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=url.long_url)