"""
app/models/analysis.py
Stores the AI-generated analysis result for a given resume.
"""

from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, Text, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False)

    ats_score: Mapped[int] = mapped_column(Integer, nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    strengths: Mapped[list] = mapped_column(JSON, nullable=True)
    weaknesses: Mapped[list] = mapped_column(JSON, nullable=True)
    missing_skills: Mapped[list] = mapped_column(JSON, nullable=True)
    suggestions: Mapped[list] = mapped_column(JSON, nullable=True)

    status: Mapped[str] = mapped_column(String(50), default="pending")
    error_message: Mapped[str] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    resume = relationship("Resume", backref="analyses")
