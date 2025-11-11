"""
Module de configuration centralisée pour l'application.

Ce module utilise Pydantic pour charger et valider la configuration
à partir des variables d'environnement et/ou d'un fichier .env.
"""

from typing import List, Union, Optional

from pydantic import AnyHttpUrl, field_validator, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Classe de configuration principale utilisant Pydantic.
    Les champs de cette classe correspondent aux variables d'environnement
    que l'application attend.
    """

    # --- Méta-informations du projet ---
    PROJECT_NAME: str = "Mon API Fantastique"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "dev"

    # --- Sécurité et JWT ---
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 jours par défaut
    ALGORITHM: str = "HS256"

    # --- Configuration de la base de données ---
    DATABASE_HOST: str = "localhost"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: SecretStr = SecretStr("changeme")
    DATABASE_NAME: str = "app_db"
    DATABASE_PORT: int = 5432

    # URI de connexion assemblée (SQLAlchemy)
    SQLALCHEMY_DATABASE_URI: Union[PostgresDsn, str] = ""

    # Validateur Pydantic pour construire l'URI de la base de données
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str, info) -> str:
        if isinstance(v, str) and v:
            return v

        password = info.data.get("DATABASE_PASSWORD")
        if isinstance(password, SecretStr):
            password = password.get_secret_value()

        return f"sqlite:///./sql_app.db"

    # --- Configuration CORS ---
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        AnyHttpUrl("http://localhost:3000"),
        AnyHttpUrl("http://localhost:8080"),
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
