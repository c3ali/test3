"""
Module de gestion de la base de données avec SQLAlchemy.

Ce module initialise le moteur SQLAlchemy, la fabrique de sessions
et la base déclarative que les modèles ORM utiliseront.
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configuration de la base de données
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./sql_app.db"
)

# Initialisation du moteur SQLAlchemy
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args
)

# Fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base déclarative pour les modèles ORM
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Générateur de session de base de données pour l'injection de dépendances.

    Yields:
        Session: Une session SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
