"""API Endpoints for authentication."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.database import get_db

router = APIRouter(tags=["auth"])


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    """
    Endpoint pour l'obtention d'un token d'accès JWT via OAuth2.
    """
    # Authentifier l'utilisateur
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ou mot de passe incorrect.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Compte utilisateur inactif."
        )

    # Créer le token JWT
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
