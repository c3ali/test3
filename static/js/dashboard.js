/**
 * Dashboard - Gestion de l'interface utilisateur
 */

// État global
const state = {
    currentBoard: null,
    currentList: null,
    boards: [],
    lists: [],
    cards: [],
};

// Sélecteurs DOM
const elements = {
    // Navigation
    navLinks: document.querySelectorAll('.nav-link'),

    // Sections
    boardsSection: document.getElementById('boards-section'),
    boardDetailSection: document.getElementById('board-detail-section'),
    apiDocsSection: document.getElementById('api-docs-section'),

    // Tableaux
    boardsGrid: document.getElementById('boards-grid'),
    btnNewBoard: document.getElementById('btn-new-board'),
    boardForm: document.getElementById('board-form'),
    boardFormSubmit: document.querySelector('#board-form form'),
    boardName: document.getElementById('board-name'),
    boardDescription: document.getElementById('board-description'),
    btnCancelBoard: document.getElementById('btn-cancel-board'),
    btnDeleteBoard: document.getElementById('btn-delete-board'),
    boardTitle: document.getElementById('board-title'),
    boardDescDisplay: document.getElementById('board-desc-display'),

    // Listes
    listsGrid: document.getElementById('lists-grid'),
    btnNewList: document.getElementById('btn-new-list'),
    listForm: document.getElementById('list-form'),
    listFormSubmit: document.querySelector('#list-form form'),
    listName: document.getElementById('list-name'),
    listDescription: document.getElementById('list-description'),
    btnCancelList: document.getElementById('btn-cancel-list'),

    // Modal
    cardModal: document.getElementById('card-modal'),
    cardTitleModal: document.getElementById('card-title-modal'),
    cardDescModal: document.getElementById('card-description-modal'),
    btnDeleteCard: document.getElementById('btn-delete-card'),

    // Toast
    toastContainer: document.getElementById('toast-container'),
};

// ============================================================================
// INITIALISATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadBoards();
});

function setupEventListeners() {
    // Navigation
    elements.navLinks.forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const section = link.dataset.section;
            showSection(section);
        });
    });

    // Tableaux
    elements.btnNewBoard.addEventListener('click', showBoardForm);
    elements.btnCancelBoard.addEventListener('click', hideBoardForm);
    elements.boardFormSubmit.addEventListener('submit', handleCreateBoard);
    elements.btnDeleteBoard.addEventListener('click', handleDeleteBoard);

    // Listes
    elements.btnNewList.addEventListener('click', showListForm);
    elements.btnCancelList.addEventListener('click', hideListForm);
    elements.listFormSubmit.addEventListener('submit', handleCreateList);

    // Modal
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', closeCardModal);
    });
    elements.cardModal.addEventListener('click', e => {
        if (e.target === elements.cardModal) closeCardModal();
    });
    elements.btnDeleteCard.addEventListener('click', handleDeleteCard);

    // Boutons retour
    document.querySelectorAll('.back-btn').forEach(btn => {
        btn.addEventListener('click', () => showSection('boards'));
    });
}

// ============================================================================
// NAVIGATION ET SECTIONS
// ============================================================================

function showSection(sectionName) {
    // Masquer toutes les sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    // Afficher la section demandée
    if (sectionName === 'boards') {
        elements.boardsSection.classList.add('active');
        loadBoards();
    } else if (sectionName === 'board-detail') {
        elements.boardDetailSection.classList.add('active');
    } else if (sectionName === 'api-docs') {
        elements.apiDocsSection.classList.add('active');
    }

    // Mettre à jour la navigation
    elements.navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.dataset.section === sectionName) {
            link.classList.add('active');
        }
    });
}

// ============================================================================
// TABLEAUX (BOARDS)
// ============================================================================

async function loadBoards() {
    try {
        elements.boardsGrid.innerHTML = '<div class="loading">Chargement...</div>';
        state.boards = await api.getBoards();
        renderBoards();
    } catch (error) {
        showToast('Erreur au chargement des tableaux', 'error');
        console.error(error);
    }
}

function renderBoards() {
    if (state.boards.length === 0) {
        elements.boardsGrid.innerHTML = '<div class="loading">Aucun tableau. Créez-en un !</div>';
        return;
    }

    elements.boardsGrid.innerHTML = state.boards.map(board => `
        <div class="board-card">
            <h3>${escapeHtml(board.name)}</h3>
            <p>${escapeHtml(board.description || 'Pas de description')}</p>
            <small style="color: #9ca3af;">Créé le ${formatDate(board.created_at)}</small>
            <div class="board-card-footer">
                <button class="btn btn-primary" onclick="viewBoard(${board.id})">Ouvrir</button>
                <button class="btn btn-danger" onclick="confirmDelete(() => deleteBoard(${board.id}))">Supprimer</button>
            </div>
        </div>
    `).join('');
}

function showBoardForm() {
    elements.boardForm.classList.remove('hidden');
    elements.boardName.focus();
}

function hideBoardForm() {
    elements.boardForm.classList.add('hidden');
    elements.boardFormSubmit.reset();
}

async function handleCreateBoard(e) {
    e.preventDefault();

    const data = {
        name: elements.boardName.value,
        description: elements.boardDescription.value || null,
    };

    try {
        await api.createBoard(data);
        showToast('Tableau créé avec succès', 'success');
        hideBoardForm();
        loadBoards();
    } catch (error) {
        showToast(`Erreur: ${error.message}`, 'error');
    }
}

async function deleteBoard(id) {
    try {
        await api.deleteBoard(id);
        showToast('Tableau supprimé', 'success');
        loadBoards();
    } catch (error) {
        showToast(`Erreur: ${error.message}`, 'error');
    }
}

async function viewBoard(id) {
    try {
        state.currentBoard = await api.getBoard(id);
        elements.boardTitle.textContent = state.currentBoard.name;
        elements.boardDescDisplay.textContent = state.currentBoard.description || 'Pas de description';
        showSection('board-detail');
        loadLists();
    } catch (error) {
        showToast(`Erreur: ${error.message}`, 'error');
    }
}

// ============================================================================
// LISTES (LISTS)
// ============================================================================

async function loadLists() {
    try {
        elements.listsGrid.innerHTML = '<div class="loading">Chargement...</div>';
        state.lists = await api.getLists();
        // Filtrer les listes du tableau courant
        state.lists = state.lists.filter(list => list.board_id === state.currentBoard.id);
        renderLists();
    } catch (error) {
        showToast('Erreur au chargement des listes', 'error');
    }
}

function renderLists() {
    if (state.lists.length === 0) {
        elements.listsGrid.innerHTML = '<div class="loading">Aucune liste. Créez-en une !</div>';
        return;
    }

    elements.listsGrid.innerHTML = state.lists.map(list => `
        <div class="list-card">
            <div class="list-header">
                <h3>${escapeHtml(list.name)}</h3>
                <button onclick="confirmDelete(() => deleteList(${list.id}))" style="font-size: 1rem;">×</button>
            </div>
            <div class="cards-container" id="cards-${list.id}">
                <div class="loading">Chargement des cartes...</div>
            </div>
            <button class="add-card-btn" onclick="showCardForm(${list.id})">
                + Ajouter une carte
            </button>
        </div>
    `).join('');

    // Charger les cartes pour chaque liste
    state.lists.forEach(list => {
        loadCards(list.id);
    });
}

function showListForm() {
    elements.listForm.classList.remove('hidden');
    elements.listName.focus();
}

function hideListForm() {
    elements.listForm.classList.add('hidden');
    elements.listFormSubmit.reset();
}

async function handleCreateList(e) {
    e.preventDefault();

    const data = {
        name: elements.listName.value,
        description: elements.listDescription.value || null,
        board_id: state.currentBoard.id,
    };

    try {
        await api.createList(data);
        showToast('Liste créée', 'success');
        hideListForm();
        loadLists();
    } catch (error) {
        showToast(`Erreur: ${error.message}`, 'error');
    }
}

async function deleteList(id) {
    try {
        await api.deleteList(id);
        showToast('Liste supprimée', 'success');
        loadLists();
    } catch (error) {
        showToast(`Erreur: ${error.message}`, 'error');
    }
}

// ============================================================================
// CARTES (CARDS)
// ============================================================================

async function loadCards(listId) {
    try {
        const cards = await api.getCards();
        const listCards = cards.filter(card => card.list_id === listId);
        renderCards(listId, listCards);
    } catch (error) {
        console.error(error);
    }
}

function renderCards(listId, cards) {
    const container = document.getElementById(`cards-${listId}`);
    if (!container) return;

    if (cards.length === 0) {
        container.innerHTML = '<div style="text-align: center; color: #9ca3af; padding: var(--spacing-md);">Aucune carte</div>';
        return;
    }

    container.innerHTML = cards.map(card => `
        <div class="card-item" onclick="viewCard(${card.id})">
            <h4>${escapeHtml(card.title)}</h4>
            <p>${escapeHtml((card.description || '').substring(0, 50))}</p>
        </div>
    `).join('');
}

function showCardForm(listId) {
    const title = prompt('Titre de la carte:');
    if (!title) return;

    const description = prompt('Description (optionnelle):');
    const data = {
        title: title,
        description: description || null,
        list_id: listId,
    };

    createCard(data);
}

async function createCard(data) {
    try {
        await api.createCard(data);
        showToast('Carte créée', 'success');
        loadLists();
    } catch (error) {
        showToast(`Erreur: ${error.message}`, 'error');
    }
}

async function viewCard(id) {
    try {
        const card = await api.getCard(id);
        state.currentCard = card;
        elements.cardTitleModal.textContent = card.title;
        elements.cardDescModal.textContent = card.description || 'Pas de description';
        openCardModal();
    } catch (error) {
        showToast(`Erreur: ${error.message}`, 'error');
    }
}

async function handleDeleteCard() {
    if (!state.currentCard) return;
    try {
        await api.deleteCard(state.currentCard.id);
        showToast('Carte supprimée', 'success');
        closeCardModal();
        loadLists();
    } catch (error) {
        showToast(`Erreur: ${error.message}`, 'error');
    }
}

function openCardModal() {
    elements.cardModal.classList.remove('hidden');
}

function closeCardModal() {
    elements.cardModal.classList.add('hidden');
    state.currentCard = null;
}

// ============================================================================
// UTILITAIRES
// ============================================================================

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    elements.toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
}

function confirmDelete(callback) {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
        callback();
    }
}

// Animation slideOut
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
