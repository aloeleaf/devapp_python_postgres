"""
Security middleware for setting security headers and CORS.
"""
from flask_cors import CORS


def setup_security_headers(app):
    """Configure security headers for all responses."""
    
    @app.after_request
    def set_security_headers(response):
        """Add security headers to every response."""
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # HSTS - Force HTTPS (adjust max-age as needed)
        if app.config.get('FLASK_ENV') == 'production':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Content Security Policy (adjust as needed)
        # This is a basic policy, customize based on your needs
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        
        return response
    
    app.logger.info('Security headers configured')


def setup_cors(app):
    """Configure CORS (Cross-Origin Resource Sharing)."""
    # Get allowed origins from config or use default
    allowed_origins = app.config.get('CORS_ORIGINS', ['http://localhost:3000'])
    
    CORS(app, 
         origins=allowed_origins,
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'X-Request-ID'],
         expose_headers=['X-Request-ID'],
         supports_credentials=True,
         max_age=3600)
    
    app.logger.info(f'CORS configured for origins: {allowed_origins}')
