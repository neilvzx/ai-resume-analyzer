"""
app/schemas/analysis.py
Response schema for AI analysis results.
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resume_id: int
    status: str
    ats_score: Optional[int]
    summary: Optional[str]
    strengths: Optional[list[str]]
    weaknesses: Optional[list[str]]
    missing_skills: Optional[list[str]]
    suggestions: Optional[list[str]]
    error_message: Optional[str]
    created_at: datetime
