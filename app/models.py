"""
Modèles SQLAlchemy pour la base de données.

Ce module définit les classes ORM qui correspondent aux tables
de la base de données.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """Modèle pour les utilisateurs."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    username = Column(String(80), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    boards = relationship("Board", back_populates="owner", cascade="all, delete-orphan")
    lists = relationship("List", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class Board(Base):
    """Modèle pour les tableaux."""
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable pour permettre usage sans auth
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    owner = relationship("User", back_populates="boards")
    lists = relationship("List", back_populates="board", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Board {self.name}>"


class List(Base):
    """Modèle pour les listes."""
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable pour permettre usage sans auth
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    board = relationship("Board", back_populates="lists")
    owner = relationship("User", back_populates="lists")
    cards = relationship("Card", back_populates="list", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<List {self.name}>"


class Card(Base):
    """Modèle pour les cartes."""
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    list = relationship("List", back_populates="cards")

    def __repr__(self):
        return f"<Card {self.title}>"
