"""
Schémas Pydantic pour la validation et sérialisation des données.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


# ===== USER SCHEMAS =====

class UserBase(BaseModel):
    """Schéma de base pour un utilisateur."""
    email: str = Field(..., description="Adresse email de l'utilisateur")
    username: str = Field(..., description="Nom d'utilisateur unique")


class UserCreate(UserBase):
    """Schéma pour la création d'un utilisateur."""
    password: str = Field(..., description="Mot de passe de l'utilisateur")


class User(UserBase):
    """Schéma pour la lecture d'un utilisateur."""
    id: int
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True


# ===== BOARD SCHEMAS =====

class BoardBase(BaseModel):
    """Schéma de base pour un tableau."""
    name: str = Field(..., min_length=1, max_length=150, description="Nom du tableau")
    description: Optional[str] = Field(None, max_length=500, description="Description du tableau")


class BoardCreate(BoardBase):
    """Schéma pour la création d'un tableau."""
    pass


class BoardUpdate(BaseModel):
    """Schéma pour la mise à jour d'un tableau."""
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=500)


class Board(BoardBase):
    """Schéma pour la lecture d'un tableau."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ===== LIST SCHEMAS =====

class ListBase(BaseModel):
    """Schéma de base pour une liste."""
    name: str = Field(..., min_length=1, max_length=150, description="Nom de la liste")
    description: Optional[str] = Field(None, max_length=500, description="Description de la liste")


class ListCreate(ListBase):
    """Schéma pour la création d'une liste."""
    board_id: int


class ListUpdate(BaseModel):
    """Schéma pour la mise à jour d'une liste."""
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=500)


class List(ListBase):
    """Schéma pour la lecture d'une liste."""
    id: int
    board_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ===== CARD SCHEMAS =====

class CardBase(BaseModel):
    """Schéma de base pour une carte."""
    title: str = Field(..., min_length=1, max_length=200, description="Titre de la carte")
    description: Optional[str] = Field(None, description="Description de la carte")


class CardCreate(CardBase):
    """Schéma pour la création d'une carte."""
    list_id: int


class CardUpdate(BaseModel):
    """Schéma pour la mise à jour d'une carte."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None


class Card(CardBase):
    """Schéma pour la lecture d'une carte."""
    id: int
    list_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ===== TOKEN SCHEMA =====

class Token(BaseModel):
    """Schéma pour la réponse de token."""
    access_token: str
    token_type: str = "bearer"
