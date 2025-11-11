# Guide de Dépannage

Ce document liste les erreurs courantes et leurs solutions.

## Erreur : "No start command was found" (Railpack)

**Symptôme :** L'application ne démarre pas sur Railway/Railpack
```
No start command was found
```

**Cause :** Railpack ne peut pas déterminer comment lancer l'application

**Solution :**
- ✅ `Procfile` existe à la racine avec : `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- ✅ `main.py` existe à la racine et importe l'app FastAPI
- ✅ `app/main.py` exporte l'objet `app` FastAPI

---

## Erreur : "PydanticImportError: BaseSettings has been moved"

**Symptôme :** Erreur à la démarrage
```
pydantic.errors.PydanticImportError: `BaseSettings` has been moved
to the `pydantic-settings` package
```

**Cause :** Pydantic v2 a déplacé `BaseSettings` vers un package séparé

**Solution :**
- ✅ Import correct : `from pydantic_settings import BaseSettings`
- ✅ `pydantic-settings==2.1.0` dans `requirements.txt`
- ✅ Validateurs mises à jour : `@field_validator` au lieu de `@validator`

---

## Erreur : "SECRET_KEY Field required"

**Symptôme :** Erreur au démarrage
```
pydantic_core._pydantic_core.ValidationError:
1 validation error for Settings
SECRET_KEY
  Field required [type=missing, input_value={}, input_type=dict]
```

**Cause :** `SECRET_KEY` est requis mais pas défini en environnement

**Solution :**
- ✅ `SECRET_KEY` a maintenant une valeur par défaut pour le développement
- ✅ **En production**, définissez une nouvelle clé sécurisée :
  ```bash
  export SECRET_KEY=$(openssl rand -hex 32)
  ```

---

## Erreur : "CORS configuration error"

**Symptôme :** Les requêtes frontend échouent avec erreur CORS

**Cause :** `BACKEND_CORS_ORIGINS` mal configurée

**Solution :**
Via le fichier `.env` ou variable d'environnement :
```env
# Format : liste d'URLs séparées par des virgules
BACKEND_CORS_ORIGINS=https://example.com,https://app.example.com
```

---

## Erreur : "Database connection refused"

**Symptôme :** L'application démarre mais ne peut pas accéder à la base de données

**Cause :** `DATABASE_URL` mal configurée ou base de données indisponible

**Solution :**
```bash
# Vérifier la connexion à la base de données
python -c "from app.database import engine; engine.connect()"

# Sur Railway, ajouter une base PostgreSQL via le dashboard
# Les variables seront automatiquement injectées
```

---

## Local Development

### Sans Docker

```bash
# 1. Créer un venv
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer un .env (optionnel, les valeurs par défaut fonctionnent)
cp .env.example .env

# 4. Lancer l'application
uvicorn app.main:app --reload
```

### Avec Docker Compose

```bash
# 1. Lancer tous les services
docker-compose up

# 2. L'app est sur http://localhost:8000
# 3. La BDD PostgreSQL est sur localhost:5432

# 4. Pour arrêter
docker-compose down
```

---

## Tests

```bash
# Tester tous les endpoints
pytest

# Avec couverture
pytest --cov=app

# Test spécifique
pytest tests/api/test_boards_api.py -v

# Mode debug
pytest -vv --tb=short
```

---

## Vérifications Pré-Déploiement

### Checklist Locale

```bash
# 1. Installation des dépendances
pip install -r requirements.txt

# 2. Lancer localement
uvicorn app.main:app --reload

# 3. Accéder à http://localhost:8000
# 4. Vérifier les docs : http://localhost:8000/docs
# 5. Health check : http://localhost:8000/health
```

### Checklist Avant Railway

```bash
# 1. Vérifier les fichiers obligatoires
ls -la | grep -E "Procfile|main.py|requirements.txt"

# 2. Vérifier que main.py à la racine existe
cat main.py | head -5

# 3. Vérifier app/main.py exporte `app`
grep "^app = FastAPI" app/main.py

# 4. Vérifier requirements.txt
cat requirements.txt | grep -E "fastapi|uvicorn|pydantic"

# 5. Tous les tests passent
pytest --tb=short
```

---

## Déploiement Railway - Pas à Pas

### 1. Configuration du Repository

```bash
git push origin main  # Push tout le code
```

### 2. Ajouter des Variables d'Environnement

Depuis le dashboard Railway :

```
ENVIRONMENT=production
SECRET_KEY=<nouvelle-clé-générée>
DATABASE_PASSWORD=<mot-de-passe-sécurisé>
```

**Générer une clé :**
```bash
openssl rand -hex 32
```

### 3. Ajouter une Base de Données

Depuis le dashboard Railway :
- Cliquez sur "New"
- Sélectionnez "Database"
- Choisissez PostgreSQL
- Les variables seront automatiquement injectées

### 4. Déploiement

Railway détecte automatiquement les changements et redéploie.

Consultez les logs :
```
Dashboard Railway → Logs → Voir les logs de déploiement
```

---

## Logs en Production

### Via Railway Dashboard

1. Allez sur votre projet
2. Cliquez sur "Deployments"
3. Ouvrez le dernier déploiement
4. Consultez les "Logs"

### Rechercher des erreurs

```
"error"
"exception"
"traceback"
"failed"
```

---

## Métriques de Santé

L'application expose deux endpoints :

```bash
# Vérifier que l'app répond
curl https://your-app.railway.app/

# Health check
curl https://your-app.railway.app/health

# Réponse attendue :
# {"status": "healthy"}
```

---

## Rollback après Erreur

Sur Railway :
1. Allez dans "Deployments"
2. Trouvez le déploiement précédent OK
3. Cliquez sur "Redeploy"

---

## Performance

### Goulot d'étranglement courant

**Symptôme :** L'app est lente ou timeout

**Solutions :**
- Augmenter la RAM/CPU dans Railway
- Ajouter du caching (Redis)
- Optimiser les requêtes BDD
- Utiliser l'index PostgreSQL

### Monitoring

Considérez d'ajouter :
- **Sentry** : Suivi des erreurs
- **DataDog** : Monitoring complet
- **Prometheus** : Métriques applicatives

---

## Questions Fréquentes

**Q: Les données sont-elles perdues lors d'un déploiement ?**
R: Non, la base de données PostgreSQL persiste. Seule l'application redémarre.

**Q: Comment mettre à jour l'app ?**
R: Committez et poussez sur main. Railway redéploiera automatiquement.

**Q: Comment activer les logs debug ?**
R: Ajoutez `--log-level debug` dans le `Procfile`

**Q: Comment limiter les requêtes ?**
R: Utilisez `slowapi` ou `ratelimit` package pour ajouter un rate limiting.

---

## Support

Documentations officielles :
- FastAPI : https://fastapi.tiangolo.com/
- Railway : https://docs.railway.app/
- Pydantic : https://docs.pydantic.dev/2.5/
- PostgreSQL : https://www.postgresql.org/docs/
