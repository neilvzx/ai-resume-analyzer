"""
app/schemas/resume.py
Response schemas for resume upload/listing.
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ResumeListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    status: str
    page_count: int
    created_at: datetime


class ResumeDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    status: str
    page_count: int
    file_size_bytes: int
    extracted_text: Optional[str]
    error_message: Optional[str]
    created_at: datetime
