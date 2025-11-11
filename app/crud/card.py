"""CRUD operations for Card model."""

from sqlalchemy.orm import Session
from app import models, schemas
from app.crud.base import CRUDBase


class CRUDCard(CRUDBase[models.Card, schemas.CardCreate, schemas.CardUpdate]):
    """CRUD operations for Card."""

    def get_by_list(self, db: Session, list_id: int, skip: int = 0, limit: int = 100):
        """Récupère toutes les cartes d'une liste."""
        return db.query(self.model).filter(
            self.model.list_id == list_id
        ).offset(skip).limit(limit).all()


card = CRUDCard(models.Card)
