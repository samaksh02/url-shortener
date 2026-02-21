from fastapi import FastAPI
from pydantic import BaseModel
import hashlib

app = FastAPI()

# Request body schema
class ShortenRequest(BaseModel):
    long_url: str

@app.get("/")
def health_check():
    return {"status": "ok"}

def getShortCode(longUrl):
    """
    Generate a deterministic short code from the long URL
    """
    hash_object = hashlib.sha256(longUrl.encode())
    # Take first 6 characters for short code
    return hash_object.hexdigest()[:6]

@app.post("/shorten")
def shorten_url(request: ShortenRequest):
    # dummy short code for now
    short_code = getShortCode(request.long_url)
    return {
        "long_url": request.long_url,
        "short_code": short_code
    }