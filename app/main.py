from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import hashlib

app = FastAPI()

# Request body schema
class ShortenRequest(BaseModel):
    long_url: str

url_map = {}

@app.get("/")
def health_check():
    return {"status": "ok"}

def generate_Short_Code(long_url) -> str:
    """
    Generate a deterministic short code from the long URL
    """
    hash_object = hashlib.sha256(long_url.encode())
    # Take first 6 characters for short code
    return hash_object.hexdigest()[:6]

@app.post("/shorten")
def shorten_url(request: ShortenRequest):
    # dummy short code for now
    short_code = generate_Short_Code(request.long_url)
    url_map[short_code] = request.long_url
    return {
        "long_url": request.long_url,
        "short_code": short_code
    }

@app.get("/{short_code}")
def redirect(short_code: str):
    if short_code not in url_map:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    long_url = url_map[short_code]
    return RedirectResponse(url=long_url)