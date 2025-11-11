"""CRUD operations for User model."""

from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserCreate]):
    """CRUD operations for User."""

    def get_by_email(self, db: Session, email: str):
        """Récupère un utilisateur par son email."""
        return db.query(self.model).filter(self.model.email == email).first()

    def get_by_username(self, db: Session, username: str):
        """Récupère un utilisateur par son nom d'utilisateur."""
        return db.query(self.model).filter(self.model.username == username).first()

    def create(self, db: Session, obj_in: schemas.UserCreate):
        """Crée un nouvel utilisateur avec mot de passe haché."""
        db_obj = self.model(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, email: str, password: str):
        """Authentifie un utilisateur."""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: models.User) -> bool:
        """Vérifie si un utilisateur est actif."""
        return user.is_active


user = CRUDUser(models.User)
