"""
Point d'entrée principal de l'application FastAPI.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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
Base.metadata.create_all(bind=engine)

# Créer l'instance de l'application FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Une API pour gérer les tableaux, listes et cartes.",
    version="1.0.0",
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

# Monter les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclure le routeur principal de l'API
app.include_router(api_router_v1.api_router, prefix=settings.API_V1_STR)

# Inclure les endpoints spécifiques
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(boards.router, prefix=settings.API_V1_STR)
app.include_router(lists.router, prefix=settings.API_V1_STR)
app.include_router(cards.router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def read_root():
    """Endpoint racine pour vérifier que l'API est en ligne."""
    return {
        "message": "Bienvenue sur l'API !",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de vérification de santé de l'application."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
