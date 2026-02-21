from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request body schema
class ShortenRequest(BaseModel):
    long_url: str

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/shorten")
def shorten_url(request: ShortenRequest):
    # dummy short code for now
    short_code = "abc123"
    return {
        "long_url": request.long_url,
        "short_code": short_code
    }