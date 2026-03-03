"""
Integration tests for API endpoints.
"""
import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_liveness(self, client):
        """Test liveness endpoint."""
        response = client.get('/health/live')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'alive'
    
    def test_readiness(self, client):
        """Test readiness endpoint."""
        response = client.get('/health/ready')
        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data
        assert 'checks' in data
    
    def test_info(self, client):
        """Test info endpoint."""
        response = client.get('/health/info')
        assert response.status_code == 200
        data = response.get_json()
        assert 'service' in data
        assert 'version' in data


class TestUserAPI:
    """Test user API endpoints."""
    
    def test_create_user(self, client):
        """Test creating a user via API."""
        response = client.post('/api/v1/users', 
                              json={'username': 'testuser', 'email': 'test@example.com'},
                              content_type='application/json')
        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['data']['username'] == 'testuser'
    
    def test_create_user_missing_fields(self, client):
        """Test creating user with missing fields."""
        response = client.post('/api/v1/users', 
                              json={'username': 'testuser'},
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_get_users(self, client):
        """Test getting users list."""
        # Create a user first
        client.post('/api/v1/users', 
                   json={'username': 'testuser', 'email': 'test@example.com'},
                   content_type='application/json')
        
        response = client.get('/api/v1/users')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'pagination' in data['data']
