"""
Module pour la gestion de la sécurité : hachage de mots de passe et JWT.
"""

import datetime
from datetime import timedelta
from typing import Any, Dict, Optional, Union

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

# Contexte pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Constantes pour la gestion des JWT
SECRET_KEY = settings.SECRET_KEY.get_secret_value()
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie qu'un mot de passe en clair correspond à un mot de passe haché.

    Args:
        plain_password (str): Le mot de passe en clair à vérifier.
        hashed_password (str): Le mot de passe haché stocké.

    Returns:
        bool: True si les mots de passe correspondent, False sinon.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Génère le hachage d'un mot de passe en clair.

    Args:
        password (str): Le mot de passe en clair à hacher.

    Returns:
        str: Le mot de passe haché.
    """
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crée un nouveau jeton d'accès JWT.

    Args:
        subject (Union[str, Any]): Le sujet du jeton (par ex., l'ID ou l'email de l'utilisateur).
        expires_delta (Optional[timedelta]): Durée de validité optionnelle du jeton.

    Returns:
        str: Le jeton JWT encodé.
    """
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode: Dict[str, Any] = {"exp": expire, "sub": str(subject)}

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Décode un jeton d'accès pour en extraire le payload.

    Args:
        token (str): Le jeton JWT à décoder.

    Returns:
        Optional[Dict[str, Any]]: Le payload du jeton si la validation est réussie, sinon None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
