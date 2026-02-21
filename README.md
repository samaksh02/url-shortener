# URL Shortener Service

A backend service that converts long URLs into short, unique links and redirects users efficiently.
Designed with scalability, reliability, and clean API design in mind.

## Features
- Shorten long URLs
- Redirect using short codes
- Persistent storage
- Basic validation

## Tech Stack
- Language: Python
- Framework: FastAPI
- Database: (to be added)
- Cache: (planned)

## API Endpoints
POST /shorten  
GET /{shortCode}

## Future Improvements
- Rate limiting
- Expiry for URLs
- Analytics (click count, timestamps)