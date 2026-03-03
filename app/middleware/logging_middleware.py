"""
Logging middleware for structured application logging.
"""
import logging
import sys
from pythonjsonlogger import jsonlogger
from flask import request, g
import time


def setup_logging(app):
    """Configure structured JSON logging for the application."""
    
    # Create logs directory if it doesn't exist
    import os
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure JSON formatter
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d'
    )
    log_handler.setFormatter(formatter)
    
    # Set log level from config or default to INFO
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    app.logger.setLevel(getattr(logging, log_level))
    
    # Add handler to app logger
    app.logger.addHandler(log_handler)
    
    # Also configure root logger for consistency
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    root_logger.addHandler(log_handler)
    
    # Request logging
    @app.before_request
    def before_request_logging():
        """Log request details before processing."""
        g.start_time = time.time()
        app.logger.info(
            'Request started',
            extra={
                'method': request.method,
                'path': request.path,
                'remote_addr': request.remote_addr,
                'request_id': g.get('request_id', 'N/A')
            }
        )
    
    @app.after_request
    def after_request_logging(response):
        """Log request details after processing."""
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            app.logger.info(
                'Request completed',
                extra={
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code,
                    'duration_ms': round(elapsed * 1000, 2),
                    'request_id': g.get('request_id', 'N/A')
                }
            )
        return response
    
    app.logger.info('Logging configured successfully')
