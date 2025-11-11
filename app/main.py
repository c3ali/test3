"""
Point d'entrée principal de l'application FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.database import Base, engine
from app.api.v1 import router as api_router_v1
from app.api.v1.endpoints import boards, lists, cards, auth

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
