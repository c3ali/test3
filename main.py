"""
Point d'entrée principal pour le déploiement.
Ce fichier permet à Railpack et autres déployeurs de détecter et lancer l'application FastAPI.
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
