"""
app/db/session.py
SQLAlchemy engine + session factory. Works against Postgres in production
(via DATABASE_URL) and SQLite for quick local testing.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# `connect_args` is only needed for SQLite (allows use across threads)
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
