# Import the Flask class from the Flask framework
from flask import Flask


# This function creates and configures our Flask application
def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # Import routes after creating the app
    from app.routes import main

    # Register the main routes with the application
    app.register_blueprint(main)

    # Return the configured Flask application
    return app