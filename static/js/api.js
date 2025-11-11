/**
 * Client API pour communiquer avec le serveur FastAPI
 */

const API_BASE = '/api/v1';

class APIClient {
    constructor() {
        this.baseUrl = API_BASE;
    }

    /**
     * Effectue une requête HTTP
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || `HTTP ${response.status}`);
            }

            // Certains endpoints retournent 204 No Content
            if (response.status === 204) {
                return null;
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error: ${endpoint}`, error);
            throw error;
        }
    }

    /**
     * =====================
     * OPERATIONS SUR BOARDS
     * =====================
     */

    async getBoards(skip = 0, limit = 100) {
        return this.request(`/boards/?skip=${skip}&limit=${limit}`);
    }

    async getBoard(id) {
        return this.request(`/boards/${id}`);
    }

    async createBoard(data) {
        return this.request('/boards/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateBoard(id, data) {
        return this.request(`/boards/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async deleteBoard(id) {
        return this.request(`/boards/${id}`, {
            method: 'DELETE',
        });
    }

    /**
     * ====================
     * OPERATIONS SUR LISTS
     * ====================
     */

    async getLists(skip = 0, limit = 100) {
        return this.request(`/lists/?skip=${skip}&limit=${limit}`);
    }

    async getList(id) {
        return this.request(`/lists/${id}`);
    }

    async createList(data) {
        return this.request('/lists/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateList(id, data) {
        return this.request(`/lists/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async deleteList(id) {
        return this.request(`/lists/${id}`, {
            method: 'DELETE',
        });
    }

    /**
     * ====================
     * OPERATIONS SUR CARDS
     * ====================
     */

    async getCards(skip = 0, limit = 100) {
        return this.request(`/cards/?skip=${skip}&limit=${limit}`);
    }

    async getCard(id) {
        return this.request(`/cards/${id}`);
    }

    async createCard(data) {
        return this.request('/cards/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateCard(id, data) {
        return this.request(`/cards/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async deleteCard(id) {
        return this.request(`/cards/${id}`, {
            method: 'DELETE',
        });
    }
}

// Exporter une instance globale
const api = new APIClient();
