"""CRUD operations for Board model."""

from sqlalchemy.orm import Session
from app import models, schemas
from app.crud.base import CRUDBase


class CRUDBoard(CRUDBase[models.Board, schemas.BoardCreate, schemas.BoardUpdate]):
    """CRUD operations for Board."""

    def get_multi_by_owner(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100):
        """Récupère tous les tableaux d'un propriétaire."""
        return db.query(self.model).filter(
            self.model.owner_id == owner_id
        ).offset(skip).limit(limit).all()

    def create_with_owner(self, db: Session, obj_in: schemas.BoardCreate, owner_id: int):
        """Crée un nouveau tableau avec le propriétaire spécifié."""
        db_obj = self.model(**obj_in.model_dump(), owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


board = CRUDBoard(models.Board)
