from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test de la route racine"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Bienvenue sur l'API VisionTech"

def test_health_check():
    """Test du health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_products():
    """Test de récupération des produits"""
    response = client.get("/api/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_product():
    """Test de récupération d'un produit unique"""
    response = client.get("/api/products/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_nonexistent_product():
    """Test de récupération d'un produit inexistant"""
    response = client.get("/api/products/9999")
    assert response.status_code == 404

def test_get_categories():
    """Test de récupération des catégories"""
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert "categories" in response.json()

def test_contact_message():
    """Test d'envoi de message de contact"""
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "Test message"
    }
    response = client.post("/api/contact", json=contact_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_create_product():
    """Test de création de produit"""
    new_product = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 10000,
        "category": "test",
        "stock": 5
    }
    response = client.post("/api/products", json=new_product)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"