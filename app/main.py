from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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

def get_short_code(long_url: str) -> str:
    return hashlib.sha256(long_url.encode()).hexdigest()[:6]

def generate_unique_short_code(db: Session, long_url: str) -> str:
    """
    Ensure short code is unique in DB (collision-safe)
    """
    base_code = get_short_code(long_url)
    short_code = base_code
    counter = 1

    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = f"{base_code}{counter}"
        counter += 1

    return short_code

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/shorten")
def shorten_url(request: ShortenRequest, db: Session = Depends(get_db)):
    # 1. Idempotency: return existing URL if already shortened
    existing = db.query(URL).filter(URL.long_url == request.long_url).first()
    if existing:
        return {
            "long_url": existing.long_url,
            "short_code": existing.short_code
        }
    
    # 2. Create new short URL safely
    try:
        short_code = generate_unique_short_code(db, request.long_url)
        url = URL(short_code=short_code, long_url=request.long_url)

        db.add(url)
        db.commit()

        return {
            "long_url": request.long_url,
            "short_code": short_code
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to shorten URL")
    
    

@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=url.long_url)