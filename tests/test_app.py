import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import app

@pytest.fixture
def client():
    """Configure le client de test Flask."""
    with app.test_client() as client:
        yield client

def test_add_contact(client):
    """Test pour l'ajout d'un contact."""
    response = client.post('/contacts', json={'name': 'John Doe', 'email': 'john.doe@example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['name'] == 'John Doe'
    assert data['email'] == 'john.doe@example.com'

def test_get_contacts(client):
    """Test pour récupérer la liste des contacts."""
    # Ajouter un contact avant de vérifier
    client.post('/contacts', json={'name': 'Jane Doe', 'email': 'jane.doe@example.com'})
    response = client.get('/contacts')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_update_contact(client):
    """Test pour la mise à jour d'un contact."""
    # Ajouter un contact d'abord
    response = client.post('/contacts', json={'name': 'John Doe', 'email': 'john.doe@example.com'})
    contact_id = response.get_json()['id']

    # Mettre à jour le contact
    response = client.put(f'/contacts/{contact_id}', json={'name': 'John Smith', 'email': 'john.smith@example.com'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'John Smith'
    assert data['email'] == 'john.smith@example.com'

def test_delete_contact(client):
    """Test pour la suppression d'un contact."""
    # Ajouter un contact avant de tester sa suppression
    response = client.post('/contacts', json={'name': 'Jane Doe', 'email': 'jane.doe@example.com'})
    contact_id = response.get_json()['id']

    # Supprimer le contact
    response = client.delete(f'/contacts/{contact_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Contact deleted'

    # Vérifier que le contact est bien supprimé
    response = client.get('/contacts')
    data = response.get_json()
    assert not any(contact['id'] == contact_id for contact in data)

def test_update_nonexistent_contact(client):
    """Test pour la mise à jour d'un contact inexistant."""
    response = client.put('/contacts/999', json={'name': 'Ghost'})
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Contact not found'

def test_delete_nonexistent_contact(client):
    """Test pour la suppression d'un contact inexistant."""
    response = client.delete('/contacts/999')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Contact deleted'

