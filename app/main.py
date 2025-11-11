"""
Point d'entrée principal de l'application FastAPI.
"""

import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import os

from app.core.config import settings
from app.database import Base, engine
from app.api.v1 import router as api_router_v1
from app.api.v1.endpoints import boards, lists, cards, auth

# Configuration du logging
logger = logging.getLogger(__name__)

# Avertissement en production si les clés par défaut sont utilisées
if settings.ENVIRONMENT == "production":
    default_secret = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    if settings.SECRET_KEY.get_secret_value() == default_secret:
        logger.warning(
            "⚠️  SECURITY WARNING: Using default SECRET_KEY in production! "
            "Generate a new key with: openssl rand -hex 32"
        )

# Créer les tables de la base de données
try:
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tables de base de données créées/vérifiées avec succès")
except Exception as e:
    logger.error(f"❌ Erreur lors de la création des tables: {e}")

# Créer l'instance de l'application FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Une API pour gérer les tableaux, listes et cartes.",
    version="1.0.0",
)

# Gestionnaires d'erreurs globaux pour renvoyer du JSON au lieu de HTML
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Gère les erreurs SQLAlchemy et renvoie du JSON."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erreur de base de données. Vérifiez le schéma ou les contraintes."}
    )

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    """Gère les erreurs d'intégrité (contraintes de BDD) et renvoie du JSON."""
    logger.error(f"Integrity error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Erreur d'intégrité des données. Vérifiez les contraintes."}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Gère toutes les autres exceptions et renvoie du JSON."""
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Erreur interne du serveur: {str(exc)}"}
    )

# Configurer CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Monter les fichiers statiques (CSS, JS, Images) - DOIT être fait AVANT les routes
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclure le routeur principal de l'API
app.include_router(api_router_v1.api_router, prefix=settings.API_V1_STR)

# Inclure les endpoints spécifiques
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(boards.router, prefix=settings.API_V1_STR)
app.include_router(lists.router, prefix=settings.API_V1_STR)
app.include_router(cards.router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de vérification de santé de l'application."""
    return {"status": "healthy"}


@app.post("/recreate-db", tags=["Admin"], include_in_schema=False)
def recreate_database():
    """
    ⚠️ ATTENTION: Recrée toutes les tables (supprime les données existantes).
    Endpoint temporaire pour migration. À SUPPRIMER en production.
    """
    try:
        # Supprimer toutes les tables
        Base.metadata.drop_all(bind=engine)
        logger.info("Tables supprimées")

        # Recréer toutes les tables avec le nouveau schéma
        Base.metadata.create_all(bind=engine)
        logger.info("Tables recréées")

        return {
            "status": "success",
            "message": "Base de données recréée avec le nouveau schéma (owner_id nullable)"
        }
    except Exception as e:
        logger.error(f"Erreur lors de la recréation: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Erreur: {str(e)}"}
        )


@app.get("/", tags=["Frontend"])
def read_root():
    """Endpoint racine - Redirige vers le dashboard."""
    static_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'dashboard.html')
    if os.path.exists(static_path):
        return FileResponse(static_path, media_type="text/html")
    return {
        "message": "Bienvenue sur l'API !",
        "docs": "/docs",
        "redoc": "/redoc",
        "dashboard": "/dashboard"
    }


@app.get("/dashboard", tags=["Frontend"])
def get_dashboard():
    """Retourne le tableau de bord."""
    static_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'dashboard.html')
    return FileResponse(static_path, media_type="text/html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
