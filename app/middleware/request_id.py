"""
Request ID middleware for tracking requests across the application.
"""
import uuid
from flask import request, g


def setup_request_id(app):
    """Add unique request ID to each request for tracing."""
    
    @app.before_request
    def add_request_id():
        """Generate or extract request ID before processing request."""
        # Check if request ID is provided in headers (e.g., from load balancer)
        request_id = request.headers.get('X-Request-ID')
        
        # Generate new ID if not provided
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # Store in g for access throughout request
        g.request_id = request_id
    
    @app.after_request
    def add_request_id_header(response):
        """Add request ID to response headers."""
        if hasattr(g, 'request_id'):
            response.headers['X-Request-ID'] = g.request_id
        return response
    
    app.logger.info('Request ID middleware configured')
