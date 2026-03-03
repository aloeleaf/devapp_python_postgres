"""
Business logic services.
Keep business logic separate from route handlers.
"""
from app.extensions import db
from app.models import User
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


class UserService:
    """Service for user-related business logic."""
    
    @staticmethod
    def create_user(username, email):
        """
        Create a new user.
        
        Args:
            username: User's username
            email: User's email address
            
        Returns:
            User object if successful, None otherwise
            
        Raises:
            ValueError: If user already exists
        """
        try:
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            logger.info(f"User created: {username}")
            return user
        except IntegrityError as e:
            db.session.rollback()
            logger.warning(f"Failed to create user {username}: {e}")
            raise ValueError("User with this username or email already exists")
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID."""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username."""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_all_users(page=1, per_page=20):
        """
        Get paginated list of users.
        
        Args:
            page: Page number (1-indexed)
            per_page: Number of results per page
            
        Returns:
            Tuple of (users, total_count)
        """
        pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """Update user fields."""
        user = User.query.get(user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        try:
            db.session.commit()
            logger.info(f"User updated: {user_id}")
            return user
        except IntegrityError as e:
            db.session.rollback()
            logger.warning(f"Failed to update user {user_id}: {e}")
            raise ValueError("Update failed - constraint violation")
    
    @staticmethod
    def delete_user(user_id):
        """Delete user by ID."""
        user = User.query.get(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        logger.info(f"User deleted: {user_id}")
        return True
