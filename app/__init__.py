# Import the Flask class from the Flask framework
from flask import Flask

# Import SQLAlchemy to connect Flask with our database
from flask_sqlalchemy import SQLAlchemy


# Create the database object
# We will use this object to create and manage database tables
db = SQLAlchemy()


# This function creates and configures our Flask application
def create_app():

    # Create a Flask application instance
    app = Flask(__name__)

    # Configure the SQLite database
    # The database file will be created inside the database folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/voting_system.db"

    # Disable unnecessary modification tracking
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Connect the database object to our Flask application
    db.init_app(app)
    # Import the User model so SQLAlchemy knows about the User table
    from app.models.user import User

    # Import the main routes after creating the application
    from app.routes import main

    # Register the main routes with the application
    app.register_blueprint(main)

    # Return the configured Flask application
    return app