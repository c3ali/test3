"""API Endpoints for managing boards."""

from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/boards", tags=["Boards"])


@router.post(
    "/",
    response_model=schemas.Board,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau tableau",
)
def create_board(
    *,
    db: Session = Depends(get_db),
    board_in: schemas.BoardCreate,
) -> Any:
    """Crée un nouveau tableau dans la base de données."""
    board = crud.board.create(db=db, obj_in=board_in)
    return board


@router.get(
    "/",
    response_model=List[schemas.Board],
    summary="Lister les tableaux",
)
def read_boards(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Récupère une liste de tableaux avec pagination."""
    boards = crud.board.get_multi(db=db, skip=skip, limit=limit)
    return boards


@router.get(
    "/{board_id}",
    response_model=schemas.Board,
    summary="Obtenir un tableau par son ID",
)
def read_board(
    *,
    db: Session = Depends(get_db),
    board_id: int,
) -> Any:
    """Récupère les détails d'un tableau spécifique."""
    board = crud.board.get(db=db, id=board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    return board


@router.put(
    "/{board_id}",
    response_model=schemas.Board,
    summary="Mettre à jour un tableau",
)
def update_board(
    *,
    db: Session = Depends(get_db),
    board_id: int,
    board_in: schemas.BoardUpdate,
) -> Any:
    """Met à jour un tableau existant."""
    board = crud.board.get(db=db, id=board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    updated_board = crud.board.update(db=db, db_obj=board, obj_in=board_in)
    return updated_board


@router.delete(
    "/{board_id}",
    response_model=schemas.Board,
    summary="Supprimer un tableau",
)
def delete_board(
    *,
    db: Session = Depends(get_db),
    board_id: int,
) -> Any:
    """Supprime un tableau de la base de données."""
    board = crud.board.get(db=db, id=board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    deleted_board = crud.board.remove(db=db, id=board_id)
    return deleted_board
