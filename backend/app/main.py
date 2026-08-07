"""
app/main.py
FastAPI application entrypoint.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.api.routes import auth, resumes, analysis

from app.models import user, resume, analysis as analysis_model  # noqa: F401

app = FastAPI(title=settings.APP_NAME)

# Allow the React dev server (and other local ports) to call this API.
app.add_middleware(
    CORSMiddleware,
    ccccccccccallow_origins=[
        "https://ai-resume-analyzer-pi-seven.vercel.app",
        "http://localhost:5173",
    ],,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}


app.include_router(auth.router)
app.include_router(resumes.router)
app.include_router(analysis.router)
