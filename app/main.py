import os
import time
from flask import Flask, jsonify
import psycopg2
from psycopg2 import OperationalError

# Initialize Flask app
app = Flask(__name__)

def get_db_connection():
    """Establishes a connection to the PostgreSQL database with retries."""
    retries = 5
    while retries > 0:
        try:
            # Use os.getenv() which is a reliable way to get environment variables
            conn = psycopg2.connect(
                host=os.getenv('POSTGRES_HOST'),
                database=os.getenv('POSTGRES_DATABASE'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                port=os.getenv('POSTGRES_PORT', '5432')
            )
            print("Successfully connected to the database.")
            return conn
        except OperationalError as err:
            print(f"Database connection failed: {err}")
            retries -= 1
            print(f"Retrying connection... ({retries} retries left)")
            time.sleep(5) # Wait 5 seconds before retrying
    return None

@app.route('/')
def hello_world():
    """A simple route to confirm the app is running."""
    return "<h1>Hello, World!</h1><p>Flask is running with Gunicorn inside Docker.</p>"

@app.route('/db_test')
def db_test():
    """
    A route to test the database connection.
    Returns a JSON response indicating success or failure.
    """
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({
            "status": "success",
            "message": "Successfully connected to the PostgreSQL database."
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to connect to the PostgreSQL database."
        }), 500

if __name__ == '__main__':
    # This block allows running the app directly with `python main.py` for local testing
    app.run(host='0.0.0.0', port=5000, debug=True)