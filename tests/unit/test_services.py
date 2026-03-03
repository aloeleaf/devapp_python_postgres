"""
Unit tests for services.
"""
import pytest
from app import create_app
from app.extensions import db
from app.services import UserService
from app.models import User


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


class TestUserService:
    """Test UserService class."""
    
    def test_create_user(self, app):
        """Test user creation."""
        with app.app_context():
            user = UserService.create_user('testuser', 'test@example.com')
            assert user is not None
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
    
    def test_create_duplicate_user(self, app):
        """Test creating duplicate user raises error."""
        with app.app_context():
            UserService.create_user('testuser', 'test@example.com')
            
            with pytest.raises(ValueError):
                UserService.create_user('testuser', 'another@example.com')
    
    def test_get_user_by_id(self, app):
        """Test getting user by ID."""
        with app.app_context():
            user = UserService.create_user('testuser', 'test@example.com')
            retrieved = UserService.get_user_by_id(user.id)
            assert retrieved is not None
            assert retrieved.id == user.id
    
    def test_get_all_users(self, app):
        """Test getting paginated users."""
        with app.app_context():
            # Create multiple users
            for i in range(5):
                UserService.create_user(f'user{i}', f'user{i}@example.com')
            
            users, total = UserService.get_all_users(page=1, per_page=10)
            assert len(users) == 5
            assert total == 5
