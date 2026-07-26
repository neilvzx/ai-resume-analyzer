"""
app/services/ai_analyzer.py
Sends resume text to Groq (OpenAI-compatible API, free tier) and returns
structured feedback.
"""

import json

from openai import OpenAI, OpenAIError

from app.core.config import settings


class AIAnalysisError(Exception):
    pass


SYSTEM_PROMPT = """You are an expert technical resume reviewer and ATS (Applicant \
Tracking System) specialist. You review resumes for software engineering and \
data roles. Always respond with ONLY a valid JSON object, no markdown fences, \
no preamble, matching exactly this schema:

{
  "ats_score": <integer 0-100, how well this resume would parse/rank in an ATS>,
  "summary": "<2-3 sentence overall assessment>",
  "strengths": ["<short strength 1>", "<short strength 2>", ...],
  "weaknesses": ["<short weakness 1>", "<short weakness 2>", ...],
  "missing_skills": ["<skill or keyword commonly expected but absent>", ...],
  "suggestions": ["<concrete, actionable improvement>", ...]
}

Keep each list to 3-6 items. Be specific and concrete, not generic."""


def _get_client() -> OpenAI:
    if not settings.GROQ_API_KEY:
        raise AIAnalysisError(
            "GROQ_API_KEY is not set. Add it to your .env file to enable AI analysis."
        )
    return OpenAI(api_key=settings.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")


def analyze_resume_text(resume_text: str) -> dict:
    client = _get_client()

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Review this resume:\n\n{resume_text}"},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )
    except OpenAIError as e:
        raise AIAnalysisError(f"Groq API call failed: {e}")

    raw_content = response.choices[0].message.content

    try:
        result = json.loads(raw_content)
    except json.JSONDecodeError as e:
        raise AIAnalysisError(f"Model did not return valid JSON: {e}")

    required_keys = {"ats_score", "summary", "strengths", "weaknesses", "missing_skills", "suggestions"}
    missing = required_keys - result.keys()
    if missing:
        raise AIAnalysisError(f"AI response missing expected fields: {missing}")

    return result
