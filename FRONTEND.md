# Documentation Frontend

## 📊 Vue d'ensemble

Le frontend est une interface Web interactive permettant de gérer des tableaux, listes et cartes en temps réel. Il communique avec l'API FastAPI via des appels REST.

## 🎨 Architecture

```
static/
├── index.html              # Page d'accueil (simple)
├── dashboard.html          # Tableau de bord interactif ← PRINCIPAL
├── css/
│   ├── style.css          # Styles de la page d'accueil
│   └── dashboard.css      # Styles du dashboard
└── js/
    ├── script.js          # Scripts de la page d'accueil
    ├── api.js             # Client API
    └── dashboard.js       # Logique du dashboard
```

## 🚀 Accès

### En Développement

```bash
uvicorn app.main:app --reload
```

Accédez à :
- **Dashboard** : http://localhost:8000/
- **Dashboard Alt** : http://localhost:8000/dashboard
- **Swagger Docs** : http://localhost:8000/docs
- **ReDoc Docs** : http://localhost:8000/redoc

### En Production

```
https://your-app.railway.app/
```

## 📋 Fonctionnalités

### 1️⃣ Gestion des Tableaux (Boards)

**Créer un tableau :**
- Cliquez sur "Nouveau Tableau"
- Entrez le nom et la description
- Cliquez sur "Créer"

**Voir les détails :**
- Cliquez sur "Ouvrir" sur une carte de tableau
- Accédez à la vue détaillée avec ses listes

**Supprimer un tableau :**
- Cliquez sur "Supprimer" sur la carte du tableau

### 2️⃣ Gestion des Listes (Lists)

**Créer une liste :**
- Ouvrez un tableau
- Cliquez sur "+ Ajouter Liste"
- Entrez le nom et la description
- Cliquez sur "Créer"

**Supprimer une liste :**
- Cliquez sur le bouton × dans l'en-tête de la liste

### 3️⃣ Gestion des Cartes (Cards)

**Créer une carte :**
- Cliquez sur "+ Ajouter une carte" sous une liste
- Entrez le titre et la description
- La carte est créée instantanément

**Voir les détails :**
- Cliquez sur une carte
- Une modal affiche les détails
- Vous pouvez la supprimer depuis la modal

**Supprimer une carte :**
- Ouvrez la modal de la carte
- Cliquez sur "Supprimer"

## 🔌 Communication API

### Client API (`js/api.js`)

Le client API centralise toute la communication avec le serveur :

```javascript
const api = new APIClient();

// Boards
await api.getBoards();
await api.getBoard(id);
await api.createBoard({ name, description });
await api.updateBoard(id, { name, description });
await api.deleteBoard(id);

// Lists
await api.getLists();
await api.createList({ name, description, board_id });
await api.deleteList(id);

// Cards
await api.getCards();
await api.createCard({ title, description, list_id });
await api.deleteCard(id);
```

### Endpoints API Utilisés

```
GET    /api/v1/boards/               Lister les tableaux
POST   /api/v1/boards/               Créer un tableau
GET    /api/v1/boards/{id}           Obtenir un tableau
PUT    /api/v1/boards/{id}           Mettre à jour
DELETE /api/v1/boards/{id}           Supprimer

GET    /api/v1/lists/                Lister les listes
POST   /api/v1/lists/                Créer une liste
DELETE /api/v1/lists/{id}            Supprimer une liste

GET    /api/v1/cards/                Lister les cartes
POST   /api/v1/cards/                Créer une carte
DELETE /api/v1/cards/{id}            Supprimer une carte
```

## 🎯 Gestion d'État

L'état global est maintenu dans `state` :

```javascript
const state = {
    currentBoard: null,      // Tableau actuellement visualisé
    currentList: null,       // Liste actuellement visualisée
    currentCard: null,       // Carte actuellement visualisée
    boards: [],              // Cache des tableaux
    lists: [],               // Cache des listes
    cards: [],               // Cache des cartes
};
```

## 🎨 Design et UX

### Thème Couleur

| Élément | Couleur |
|---------|---------|
| Primary | Bleu (#2563eb) |
| Success | Vert (#10b981) |
| Danger | Rouge (#ef4444) |
| Background | Gris clair (#f9fafb) |
| Text | Gris foncé (#1f2937) |

### Responsive Design

- **Desktop** : Grille multi-colonnes
- **Tablet** : Grille 2 colonnes
- **Mobile** : Grille 1 colonne

Les éléments s'adaptent automatiquement.

### Notifications Toast

Les notifications pop-up en haut à droite informent l'utilisateur des opérations :

- ✅ **Success** (vert) : Opération réussie
- ❌ **Error** (rouge) : Erreur
- ℹ️ **Info** (bleu) : Information

Les notifications disparaissent automatiquement après 3 secondes.

## 🔧 Développement

### Ajouter une Nouvelle Fonctionnalité

**1. Créer un endpoint API** (`app/api/v1/endpoints/`):
```python
@router.post("/items/")
def create_item(item_in: schemas.ItemCreate):
    return crud.item.create(db=db, obj_in=item_in)
```

**2. Ajouter une méthode au client API** (`js/api.js`):
```javascript
async createItem(data) {
    return this.request('/items/', {
        method: 'POST',
        body: JSON.stringify(data),
    });
}
```

**3. Ajouter la logique UI** (`js/dashboard.js`):
```javascript
async function handleCreateItem(e) {
    e.preventDefault();
    const data = { ... };
    const item = await api.createItem(data);
    showToast('Item créé', 'success');
    // Rafraîchir l'UI
}
```

**4. Mettre à jour le HTML** (`dashboard.html`):
```html
<button onclick="handleCreateItem()">Créer Item</button>
```

### Débogage

**Console Navigateur** :
Ouvrez la DevTools (F12) pour voir :
- Les appels API
- Les erreurs JavaScript
- L'état de l'application

**Logs API** :
Les logs du serveur sont affichés en terminal :
```
INFO:     GET /api/v1/boards/ 200 OK
```

## 🔒 Sécurité

### Validation Côté Client

Le frontend valide les entrées avant d'envoyer à l'API.

### Validation Côté Serveur

L'API valide également toutes les données avec Pydantic.

### Protection XSS

Les données utilisateur sont echappées (escaped) avant d'être affichées :
```javascript
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

## 📱 Mobile

Le dashboard est entièrement responsive :

- Navigation adaptée sur petits écrans
- Grille d'une colonne sur mobile
- Buttons tactiles facilement cliquables
- Formulaires optimisés pour le mobile

## 🚧 Limitations Connues

- Pas d'authentification (à implémenter)
- Pas de drag-and-drop entre listes
- Pas de recherche ou filtrage
- Pas de pagination (chargement limité à 100)
- Pas de synchronisation multi-utilisateurs

## 📚 Améliorations Futures

- [ ] Ajouter la recherche de cartes
- [ ] Implémenter le drag-and-drop
- [ ] Ajouter des filtres et des tags
- [ ] Support du multi-utilisateurs
- [ ] Synchronisation temps réel (WebSockets)
- [ ] Système d'authentification
- [ ] Export des données
- [ ] Collaboration en temps réel
- [ ] Dark mode
- [ ] Intégration des fichiers

## 📖 Ressources

- **Swagger API Docs** : `/docs`
- **ReDoc Docs** : `/redoc`
- **Code API Client** : `js/api.js`
- **Code Dashboard** : `js/dashboard.js`
- **CSS** : `css/dashboard.css`

## 💬 Support

En cas de problème avec le frontend :

1. Vérifiez la console navigateur (F12)
2. Vérifiez les logs serveur
3. Accédez à `/docs` pour tester l'API directement
4. Consultez `TROUBLESHOOTING.md` pour les erreurs courantes
