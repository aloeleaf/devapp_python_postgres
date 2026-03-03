"""
API v1 routes example.
Versioned API endpoints for better API management.
"""
from flask import Blueprint, request
from app.services import UserService
from app.schemas import user_schema, users_schema, pagination_schema
from app.utils import success_response, error_response, validate_json, paginate_response
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@api_v1_bp.route('/users', methods=['GET'])
def get_users():
    """Get paginated list of users."""
    try:
        # Validate pagination parameters
        pagination_params = pagination_schema.load(request.args)
        page = pagination_params['page']
        per_page = pagination_params['per_page']
        
        # Get users from service
        users, total = UserService.get_all_users(page=page, per_page=per_page)
        
        # Serialize users
        users_data = users_schema.dump(users)
        
        # Create paginated response
        response_data = paginate_response(users_data, total, page, per_page)
        
        return success_response(response_data)
        
    except ValidationError as e:
        return error_response('Invalid parameters', 400, e.messages)
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return error_response('Failed to retrieve users', 500)


@api_v1_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID."""
    try:
        user = UserService.get_user_by_id(user_id)
        if not user:
            return error_response('User not found', 404)
        
        user_data = user_schema.dump(user)
        return success_response(user_data)
        
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        return error_response('Failed to retrieve user', 500)


@api_v1_bp.route('/users', methods=['POST'])
@validate_json('username', 'email')
def create_user():
    """Create a new user."""
    try:
        data = request.get_json()
        
        # Validate input
        validated_data = user_schema.load(data)
        
        # Create user
        user = UserService.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        
        user_data = user_schema.dump(user)
        return success_response(user_data, 'User created successfully', 201)
        
    except ValidationError as e:
        return error_response('Validation failed', 400, e.messages)
    except ValueError as e:
        return error_response(str(e), 409)
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return error_response('Failed to create user', 500)


@api_v1_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user."""
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided', 400)
        
        # Validate input (partial update allowed)
        validated_data = user_schema.load(data, partial=True)
        
        # Update user
        user = UserService.update_user(user_id, **validated_data)
        
        if not user:
            return error_response('User not found', 404)
        
        user_data = user_schema.dump(user)
        return success_response(user_data, 'User updated successfully')
        
    except ValidationError as e:
        return error_response('Validation failed', 400, e.messages)
    except ValueError as e:
        return error_response(str(e), 409)
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        return error_response('Failed to update user', 500)


@api_v1_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    try:
        success = UserService.delete_user(user_id)
        
        if not success:
            return error_response('User not found', 404)
        
        return success_response(message='User deleted successfully')
        
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        return error_response('Failed to delete user', 500)
