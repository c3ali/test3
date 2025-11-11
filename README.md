# Application FastAPI - Gestion de Tableaux, Listes et Cartes

Une application web moderne construite avec **FastAPI** pour gérer des tableaux, des listes et des cartes (style Trello/Kanban).

## Fonctionnalités

- ✅ Gestion complète des tableaux (CRUD)
- ✅ Gestion des listes au sein des tableaux
- ✅ Gestion des cartes au sein des listes
- ✅ API REST avec documentation automatique Swagger
- ✅ Frontend statique (HTML, CSS, JavaScript)
- ✅ Authentification JWT (préparée)
- ✅ Tests unitaires avec pytest

## Structure du Projet

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── boards.py
│   │       │   ├── lists.py
│   │       │   └── cards.py
│   │       └── router.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── base.py
│   │   ├── board.py
│   │   ├── list.py
│   │   ├── card.py
│   │   └── user.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
├── static/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── tests/
│   ├── conftest.py
│   └── api/
│       └── test_boards_api.py
├── requirements.txt
└── .env.example
```

## Installation

### Prérequis

- Python 3.8+
- pip

### Étapes

1. **Cloner le répertoire** :
   ```bash
   git clone <url-du-repo>
   cd <nom-du-repo>
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer l'environnement** :
   ```bash
   cp .env.example .env
   # Éditez .env selon vos besoins
   ```

5. **Lancer l'application** :
   ```bash
   uvicorn app.main:app --reload
   ```

   L'API sera disponible sur `http://localhost:8000`

## Utilisation

### API REST

- **Documentation interactive (Swagger)** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **Documentation alternative (ReDoc)** : [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Endpoints principaux

#### Tableaux (Boards)
- `GET /api/v1/boards/` - Lister tous les tableaux
- `POST /api/v1/boards/` - Créer un nouveau tableau
- `GET /api/v1/boards/{id}` - Obtenir un tableau
- `PUT /api/v1/boards/{id}` - Mettre à jour un tableau
- `DELETE /api/v1/boards/{id}` - Supprimer un tableau

#### Listes
- `GET /api/v1/lists/` - Lister toutes les listes
- `POST /api/v1/lists/` - Créer une nouvelle liste
- `GET /api/v1/lists/{id}` - Obtenir une liste
- `PUT /api/v1/lists/{id}` - Mettre à jour une liste
- `DELETE /api/v1/lists/{id}` - Supprimer une liste

#### Cartes
- `GET /api/v1/cards/` - Lister toutes les cartes
- `POST /api/v1/cards/` - Créer une nouvelle carte
- `GET /api/v1/cards/{id}` - Obtenir une carte
- `PUT /api/v1/cards/{id}` - Mettre à jour une carte
- `DELETE /api/v1/cards/{id}` - Supprimer une carte

## Tests

Pour exécuter les tests :

```bash
pytest
```

Pour voir la couverture des tests :

```bash
pytest --cov=app
```

## Configuration

Les paramètres de l'application sont gérés dans `app/core/config.py` et peuvent être configurés via des variables d'environnement (fichier `.env`).

### Variables importantes :

- `SECRET_KEY` : Clé secrète pour la signature JWT
- `DATABASE_URL` : URL de connexion à la base de données
- `ENVIRONMENT` : Environnement (dev, staging, prod)
- `BACKEND_CORS_ORIGINS` : Origines CORS autorisées

## Architecture

L'application suit une architecture en couches :

- **API Layer** (`app/api/`) : Endpoints HTTP et validation des données
- **CRUD Layer** (`app/crud/`) : Opérations de base de données
- **Models** (`app/models.py`) : Modèles SQLAlchemy
- **Schemas** (`app/schemas.py`) : Schémas Pydantic pour la validation
- **Core** (`app/core/`) : Utilitaires (configuration, sécurité)

## Frontend

Un front-end simple est fourni dans le répertoire `static/` :

- **index.html** : Page d'accueil
- **css/style.css** : Styles CSS
- **js/script.js** : JavaScript côté client

## Contributions

Les contributions sont les bienvenues ! Veuillez créer une branche feature et soumettre une pull request.

## Licence

Ce projet est fourni à titre d'exemple éducatif.
