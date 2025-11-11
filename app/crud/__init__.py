"""CRUD operations for the application."""

from app.crud.board import board
from app.crud.list import list_
from app.crud.card import card
from app.crud.user import user

# Export avec un alias pour éviter le conflit avec le mot-clé 'list'
list = list_

__all__ = ["board", "list", "card", "user"]
