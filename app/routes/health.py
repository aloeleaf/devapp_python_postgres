"""
Health check and monitoring endpoints.
Used by load balancers and monitoring systems.
"""
from flask import Blueprint, jsonify, current_app
from sqlalchemy import text
from app.extensions import db
import sys

health_bp = Blueprint('health', __name__, url_prefix='/health')


@health_bp.route('/live', methods=['GET'])
def liveness():
    """
    Liveness probe - indicates if the application is running.
    Used by Kubernetes/Docker to know if container should be restarted.
    """
    return jsonify({
        'status': 'alive',
        'service': 'dev_app_flask_postgresdb'
    }), 200


@health_bp.route('/ready', methods=['GET'])
def readiness():
    """
    Readiness probe - indicates if the application is ready to serve traffic.
    Checks database connectivity and other dependencies.
    """
    checks = {
        'database': False,
        'overall': False
    }
    
    # Check database connection
    try:
        db.session.execute(text('SELECT 1'))
        checks['database'] = True
    except Exception as e:
        current_app.logger.error(f"Database health check failed: {e}")
        checks['database'] = False
    
    # Overall status - all checks must pass
    checks['overall'] = all([
        checks['database']
    ])
    
    status_code = 200 if checks['overall'] else 503
    
    return jsonify({
        'status': 'ready' if checks['overall'] else 'not_ready',
        'checks': checks,
        'service': 'dev_app_flask_postgresdb'
    }), status_code


@health_bp.route('/info', methods=['GET'])
def info():
    """
    Application information endpoint.
    Provides version, environment, and configuration info.
    """
    return jsonify({
        'service': 'dev_app_flask_postgresdb',
        'version': '1.0.0',
        'environment': current_app.config.get('FLASK_ENV', 'unknown'),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'debug_mode': current_app.debug
    }), 200
