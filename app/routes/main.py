from flask import Blueprint, jsonify
from sqlalchemy import text
from app.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def hello():
    return "<h1>Hello from the Application Factory!</h1>"

@main_bp.route('/db_test')
def db_test():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({"status": "success", "message": "Connected to DB"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
