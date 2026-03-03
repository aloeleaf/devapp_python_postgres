"""
Utility functions and helpers.
"""
from flask import jsonify
from functools import wraps
import logging

logger = logging.getLogger(__name__)


def success_response(data=None, message=None, status_code=200):
    """
    Create a standardized success response.
    
    Args:
        data: Response data (dict, list, or None)
        message: Optional success message
        status_code: HTTP status code (default 200)
        
    Returns:
        Flask JSON response
    """
    response = {
        'status': 'success'
    }
    
    if message:
        response['message'] = message
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code


def error_response(message, status_code=400, errors=None):
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        status_code: HTTP status code (default 400)
        errors: Optional detailed error information
        
    Returns:
        Flask JSON response
    """
    response = {
        'status': 'error',
        'message': message
    }
    
    if errors:
        response['errors'] = errors
    
    return jsonify(response), status_code


def validate_json(*required_fields):
    """
    Decorator to validate JSON request data.
    
    Usage:
        @validate_json('username', 'email')
        def create_user():
            # handler code
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            from flask import request
            
            if not request.is_json:
                return error_response('Request must be JSON', 400)
            
            data = request.get_json()
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return error_response(
                    'Missing required fields',
                    400,
                    {'missing_fields': missing_fields}
                )
            
            return f(*args, **kwargs)
        return wrapper
    return decorator


def paginate_response(items, total, page, per_page):
    """
    Create a paginated response.
    
    Args:
        items: List of items for current page
        total: Total number of items
        page: Current page number
        per_page: Items per page
        
    Returns:
        Dictionary with pagination metadata
    """
    import math
    
    return {
        'items': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_items': total,
            'total_pages': math.ceil(total / per_page) if per_page > 0 else 0,
            'has_next': page * per_page < total,
            'has_prev': page > 1
        }
    }
