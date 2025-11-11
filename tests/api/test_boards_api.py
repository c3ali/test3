"""
Tests pour les endpoints de gestion des tableaux.
"""

import pytest


class TestCreateBoard:
    """Tests pour la création de board (POST /api/v1/boards)."""

    def test_create_board_success(self, client):
        """Vérifie la création réussie d'un board avec des données valides."""
        payload = {
            "name": "Projet Phoenix",
            "description": "Tableau de suivi pour le projet Phoenix."
        }

        response = client.post("/api/v1/boards/", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["description"] == payload["description"]
        assert "id" in data

    def test_create_board_missing_name(self, client):
        """Vérifie que la création échoue si le champ 'name' est manquant."""
        payload = {"description": "Un tableau sans nom."}

        response = client.post("/api/v1/boards/", json=payload)

        assert response.status_code == 422


class TestGetBoards:
    """Tests pour la lecture des boards."""

    def test_get_all_boards_empty(self, client):
        """Vérifie qu'une liste vide est retournée."""
        response = client.get("/api/v1/boards/")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_boards_with_data(self, client):
        """Vérifie que la liste des boards est retournée correctement."""
        # Créer deux boards
        client.post("/api/v1/boards/", json={"name": "Board A", "description": ""})
        client.post("/api/v1/boards/", json={"name": "Board B", "description": ""})

        response = client.get("/api/v1/boards/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    def test_get_one_board_success(self, client):
        """Vérifie la récupération d'un board spécifique."""
        # Créer un board
        create_response = client.post(
            "/api/v1/boards/",
            json={"name": "Board Test", "description": "Détails"}
        )
        board_id = create_response.json()["id"]

        response = client.get(f"/api/v1/boards/{board_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == board_id
        assert data["name"] == "Board Test"

    def test_get_one_board_not_found(self, client):
        """Vérifie qu'une erreur 404 est retournée."""
        response = client.get("/api/v1/boards/9999")

        assert response.status_code == 404


class TestUpdateBoard:
    """Tests pour la mise à jour d'un board."""

    def test_update_board_success(self, client):
        """Vérifie la mise à jour réussie d'un board."""
        # Créer un board
        create_response = client.post(
            "/api/v1/boards/",
            json={"name": "Ancien Nom", "description": ""}
        )
        board_id = create_response.json()["id"]

        # Mettre à jour
        payload = {"name": "Nouveau Nom du Board"}
        response = client.put(f"/api/v1/boards/{board_id}", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Nouveau Nom du Board"

    def test_update_board_not_found(self, client):
        """Vérifie qu'une erreur 404 est retournée."""
        response = client.put(
            "/api/v1/boards/9999",
            json={"name": "N'existera jamais"}
        )

        assert response.status_code == 404


class TestDeleteBoard:
    """Tests pour la suppression d'un board."""

    def test_delete_board_success(self, client):
        """Vérifie la suppression réussie d'un board."""
        # Créer un board
        create_response = client.post(
            "/api/v1/boards/",
            json={"name": "À Supprimer", "description": ""}
        )
        board_id = create_response.json()["id"]

        # Supprimer
        response = client.delete(f"/api/v1/boards/{board_id}")

        assert response.status_code == 200

        # Vérifier que le board a été supprimé
        get_response = client.get(f"/api/v1/boards/{board_id}")
        assert get_response.status_code == 404

    def test_delete_board_not_found(self, client):
        """Vérifie qu'une erreur 404 est retournée."""
        response = client.delete("/api/v1/boards/9999")

        assert response.status_code == 404
