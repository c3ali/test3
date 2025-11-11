"""CRUD operations for List model."""

from sqlalchemy.orm import Session
from app import models, schemas
from app.crud.base import CRUDBase


class CRUDList(CRUDBase[models.List, schemas.ListCreate, schemas.ListUpdate]):
    """CRUD operations for List."""

    def get_multi_by_owner(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100):
        """Récupère toutes les listes d'un propriétaire."""
        return db.query(self.model).filter(
            self.model.owner_id == owner_id
        ).offset(skip).limit(limit).all()

    def create_with_owner(self, db: Session, obj_in: schemas.ListCreate, owner_id: int):
        """Crée une nouvelle liste avec le propriétaire spécifié."""
        obj_data = obj_in.model_dump()
        obj_data["owner_id"] = owner_id
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


list_ = CRUDList(models.List)
