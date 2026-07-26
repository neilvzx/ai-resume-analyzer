"""
app/api/routes/analysis.py
Trigger AI analysis on a parsed resume, and fetch past analysis results.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisResponse
from app.services.ai_analyzer import analyze_resume_text, AIAnalysisError

router = APIRouter(prefix="/api/resumes", tags=["analysis"])


@router.post("/{resume_id}/analyze", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def analyze_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.owner_id == current_user.id)
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if resume.status != "parsed" or not resume.extracted_text:
        raise HTTPException(
            status_code=400,
            detail=f"Resume is not ready for analysis (status: {resume.status})",
        )

    analysis = Analysis(resume_id=resume.id, status="pending")
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    try:
        result = analyze_resume_text(resume.extracted_text)
        analysis.ats_score = result["ats_score"]
        analysis.summary = result["summary"]
        analysis.strengths = result["strengths"]
        analysis.weaknesses = result["weaknesses"]
        analysis.missing_skills = result["missing_skills"]
        analysis.suggestions = result["suggestions"]
        analysis.status = "completed"
    except AIAnalysisError as e:
        analysis.status = "failed"
        analysis.error_message = str(e)

    db.commit()
    db.refresh(analysis)

    if analysis.status == "failed":
        raise HTTPException(status_code=502, detail=analysis.error_message)

    return analysis


@router.get("/{resume_id}/analyses", response_model=list[AnalysisResponse])
def list_analyses(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.owner_id == current_user.id)
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return (
        db.query(Analysis)
        .filter(Analysis.resume_id == resume_id)
        .order_by(Analysis.created_at.desc())
        .all()
    )
