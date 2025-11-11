"""API Endpoints for managing cards."""

from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/cards", tags=["Cards"])


@router.get(
    "/",
    response_model=List[schemas.Card],
    summary="Lister les cartes",
)
def read_cards(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Récupère une liste de cartes avec pagination."""
    cards = crud.card.get_multi(db=db, skip=skip, limit=limit)
    return cards


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Card,
    summary="Créer une nouvelle carte",
)
def create_card(
    *,
    db: Session = Depends(get_db),
    card_in: schemas.CardCreate,
) -> Any:
    """Crée une nouvelle carte."""
    card = crud.card.create(db=db, obj_in=card_in)
    return card


@router.get(
    "/{id}",
    response_model=schemas.Card,
    summary="Obtenir une carte par son ID",
)
def read_card(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """Récupère une carte spécifique."""
    card = crud.card.get(db=db, id=id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La carte n'a pas été trouvée.",
        )
    return card


@router.put(
    "/{id}",
    response_model=schemas.Card,
    summary="Mettre à jour une carte",
)
def update_card(
    *,
    db: Session = Depends(get_db),
    id: int,
    card_in: schemas.CardUpdate,
) -> Any:
    """Met à jour une carte existante."""
    card = crud.card.get(db=db, id=id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La carte n'a pas été trouvée.",
        )
    card = crud.card.update(db=db, db_obj=card, obj_in=card_in)
    return card


@router.delete(
    "/{id}",
    response_model=schemas.Card,
    summary="Supprimer une carte",
)
def delete_card(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """Supprime une carte."""
    card = crud.card.get(db=db, id=id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La carte n'a pas été trouvée.",
        )

    card = crud.card.remove(db=db, id=id)
    return card
