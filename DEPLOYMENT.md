# Guide de Déploiement

Ce document explique comment déployer l'application FastAPI sur différentes plateformes.

## 🚀 Options de Déploiement

### 1. Railway (Recommandé)

Railway est une plateforme de déploiement moderne et simple.

**Étapes :**

1. Connectez votre repo GitHub à Railway (https://railway.app)
2. Railway détectera automatiquement que c'est une application Python
3. Il utilisera le `Procfile` pour lancer l'application
4. Les variables d'environnement peuvent être définies via le dashboard Railway

**Configuration automatique :**
- Railway lit le `Procfile` et exécute : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Le port est automatiquement exposé
- Les logs sont accessibles via le dashboard

**Ajouter une base de données PostgreSQL :**
```bash
# Via le dashboard Railway :
# 1. Cliquez sur "New"
# 2. Sélectionnez "Database"
# 3. Choisissez PostgreSQL
# 4. Les variables d'environnement seront automatiquement injectées
```

---

### 2. Heroku

Heroku utilise également le `Procfile`.

**Étapes :**

```bash
# 1. Installer Heroku CLI
# 2. Se connecter
heroku login

# 3. Créer une application
heroku create <nom-app>

# 4. Ajouter PostgreSQL (optionnel)
heroku addons:create heroku-postgresql:hobby-dev

# 5. Déployer
git push heroku main

# 6. Voir les logs
heroku logs --tail
```

---

### 3. Docker (Local ou Serveur)

Utilisez Docker pour une déploiement cohérent sur n'importe quel serveur.

**Avec Docker Compose (Développement Local) :**

```bash
# Lancer l'application complète avec PostgreSQL
docker-compose up

# L'app sera disponible sur http://localhost:8000
# PostgreSQL sur localhost:5432
```

**Construction manuelle :**

```bash
# Construire l'image
docker build -t mon-api .

# Lancer un container
docker run -p 8000:8000 \
  -e SECRET_KEY=<clé-secrète> \
  -e DATABASE_URL=postgresql://... \
  mon-api
```

**Avec Docker Hub :**

```bash
# Taguer l'image
docker tag mon-api username/mon-api:latest

# Pousser vers Docker Hub
docker push username/mon-api:latest

# Puis tirer et lancer depuis n'importe quel serveur
docker run -p 8000:8000 username/mon-api:latest
```

---

### 4. Vercel

Vercel supporte les API FastAPI.

**Étapes :**

1. Créez un fichier `vercel.json` :

```json
{
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb",
        "runtime": "python3.11"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ]
}
```

2. Connectez votre GitHub à Vercel
3. Vercel déploiera automatiquement à chaque push

**Note :** Vercel utilise des "Serverless Functions", ce qui peut avoir des limitations pour les applications long-running.

---

### 5. Render

Render est une excellente alternative à Heroku.

**Étapes :**

1. Allez sur https://render.com
2. Créez un "New Web Service"
3. Connectez votre repo GitHub
4. Configurez :
   - **Build Command :** `pip install -r requirements.txt`
   - **Start Command :** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Ajoutez une base de données PostgreSQL

---

### 6. DigitalOcean / AWS / GCP (Serveur Classique)

Pour les serveurs VPS classiques :

```bash
# 1. SSH sur votre serveur
ssh user@your-server.com

# 2. Installer Python et dépendances
sudo apt-get update
sudo apt-get install python3.11 python3-pip postgresql

# 3. Cloner le repo
git clone <url-du-repo>
cd mon-app

# 4. Créer un venv
python3 -m venv venv
source venv/bin/activate

# 5. Installer les dépendances
pip install -r requirements.txt

# 6. Configurer .env
cp .env.example .env
nano .env  # Éditer avec vos vraies valeurs

# 7. Créer un service systemd
sudo nano /etc/systemd/system/mon-app.service
```

**Contenu du fichier `/etc/systemd/system/mon-app.service` :**

```ini
[Unit]
Description=Mon Application FastAPI
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/user/mon-app
Environment="PATH=/home/user/mon-app/venv/bin"
ExecStart=/home/user/mon-app/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 8. Démarrer le service
sudo systemctl daemon-reload
sudo systemctl start mon-app
sudo systemctl enable mon-app

# 9. Configurer Nginx comme reverse proxy
sudo apt-get install nginx
# Éditer /etc/nginx/sites-available/default
# pour proxifier vers http://localhost:8000
```

---

## 🔐 Variables d'Environnement

Voici les variables d'environnement nécessaires :

```env
# Méta
PROJECT_NAME=Mon API Fantastique
ENVIRONMENT=production

# Sécurité (générez une nouvelle clé !)
SECRET_KEY=<valeur-cryptographiquement-sécurisée>
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256

# Base de données
DATABASE_HOST=your-db-host
DATABASE_USER=postgres
DATABASE_PASSWORD=<mot-de-passe-sécurisé>
DATABASE_NAME=app_db
DATABASE_PORT=5432

# CORS
BACKEND_CORS_ORIGINS=https://example.com,https://app.example.com
```

### Générer une clé secrète sécurisée :

```bash
# Linux/Mac
openssl rand -hex 32

# Python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🧪 Tests Avant Déploiement

Avant de déployer, testez votre application :

```bash
# 1. Tests unitaires
pytest

# 2. Vérifier la couverture
pytest --cov=app

# 3. Lancer localement
uvicorn app.main:app --reload

# 4. Tester avec Docker Compose
docker-compose up
# Visitez http://localhost:8000/docs
```

---

## 📋 Checklist de Déploiement

- [ ] `SECRET_KEY` est défini et sécurisé
- [ ] `ENVIRONMENT` est défini à `production`
- [ ] `DATABASE_URL` pointe vers une base de données en production
- [ ] `BACKEND_CORS_ORIGINS` est configuré correctement
- [ ] Les tests passent : `pytest`
- [ ] L'application fonctionne localement : `uvicorn app.main:app --reload`
- [ ] Les logs de l'application sont vérifiés
- [ ] Un monitoring est mis en place
- [ ] Les backups de la base de données sont configurés
- [ ] Un plan de rollback est en place

---

## 🆘 Dépannage

### "No start command was found"

**Solution :** Vérifiez que `Procfile` existe à la racine du projet avec le contenu correct.

### Application impossible à démarrer

```bash
# Voir les logs localement
uvicorn app.main:app --reload --log-level debug

# Vérifier que main.py à la racine existe
cat main.py
```

### Erreur de base de données

```bash
# Vérifier la connexion à la BDD
python -c "from app.database import engine; print(engine)"

# Vérifier que les tables sont créées
# app/main.py exécute : Base.metadata.create_all(bind=engine)
```

### Port déjà utilisé

```bash
# Utiliser un autre port
uvicorn app.main:app --port 8001
```

---

## 📊 Monitoring en Production

### Logs
- Railway : Dashboard → Logs
- Heroku : `heroku logs --tail`
- Serveur custom : `/var/log/` ou sortie du service systemd

### Endpoints de santé

L'application expose deux endpoints pour le monitoring :

```bash
# Endpoint racine
curl https://your-app.com/

# Vérification de santé
curl https://your-app.com/health
```

### Métriques et Alertes

Considérez d'ajouter :
- **Sentry** pour le suivi des erreurs
- **DataDog** ou **New Relic** pour le monitoring
- **Prometheus** pour les métriques applicatives

---

## 🔄 Mise à Jour en Production

```bash
# 1. Faire un commit et un push
git add .
git commit -m "Your message"
git push origin main

# 2. La plupart des platforms déploient automatiquement
# Railway et Heroku : redéploiement automatique
# Serveur custom : `git pull` et redémarrer le service

# 3. Vérifier que l'app est ok
curl https://your-app.com/health
```

---

**Besoin d'aide ?** Consultez la documentation officielle :
- FastAPI : https://fastapi.tiangolo.com/deployment/
- Railway : https://docs.railway.app/
- Heroku : https://devcenter.heroku.com/
