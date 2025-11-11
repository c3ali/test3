"""API Endpoints for managing lists."""

from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/lists", tags=["Lists"])


@router.get(
    "/",
    response_model=List[schemas.List],
    summary="Lister les listes",
)
def read_lists(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Récupère une liste de listes avec pagination."""
    lists = crud.list_.get_multi(db=db, skip=skip, limit=limit)
    return lists


@router.post(
    "/",
    response_model=schemas.List,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une nouvelle liste",
)
def create_list(
    *,
    db: Session = Depends(get_db),
    list_in: schemas.ListCreate,
) -> Any:
    """Crée une nouvelle liste."""
    new_list = crud.list_.create(db=db, obj_in=list_in)
    return new_list


@router.get(
    "/{id}",
    response_model=schemas.List,
    summary="Obtenir une liste par son ID",
)
def read_list(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """Récupère une liste spécifique par son ID."""
    db_list = crud.list_.get(db=db, id=id)
    if not db_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )
    return db_list


@router.put(
    "/{id}",
    response_model=schemas.List,
    summary="Mettre à jour une liste",
)
def update_list(
    *,
    db: Session = Depends(get_db),
    id: int,
    list_in: schemas.ListUpdate,
) -> Any:
    """Met à jour une liste existante."""
    db_list = crud.list_.get(db=db, id=id)
    if not db_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )
    updated_list = crud.list_.update(db=db, db_obj=db_list, obj_in=list_in)
    return updated_list


@router.delete(
    "/{id}",
    response_model=schemas.List,
    summary="Supprimer une liste",
)
def delete_list(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """Supprime une liste."""
    db_list = crud.list_.get(db=db, id=id)
    if not db_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )
    deleted_list = crud.list_.remove(db=db, id=id)
    return deleted_list
