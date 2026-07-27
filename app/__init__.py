# Import the Flask class from the Flask framework
from flask import Flask

# Import SQLAlchemy to connect Flask with our database
from flask_sqlalchemy import SQLAlchemy

# Import LoginManager to manage user login sessions
from flask_login import LoginManager


# Create the database object
# We will use this object to create and manage database tables
db = SQLAlchemy()


# Create the login manager object
# This will manage user login sessions
login_manager = LoginManager()

# Set the page where unauthenticated users should be redirected
login_manager.login_view = "auth.login"
@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))


# This function creates and configures our Flask application
def create_app():

    # Create a Flask application instance
    app = Flask(__name__)

    print("Flask template folder:", app.template_folder)
    print("Flask template path:", app.jinja_loader.searchpath)

    # Configure the SQLite database
    # The database file will be created inside the database folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/voting_system.db"

    # Disable unnecessary modification tracking
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Connect the database object to our Flask application
    db.init_app(app)

    # Connect Flask-Login to our Flask application
    login_manager.init_app(app)

    # Import the User model so SQLAlchemy knows about the User table
    from app.models.user import User

    # Import the main routes after creating the application
    from app.routes import main

    # Register the main routes with the application
    app.register_blueprint(main)

    # Import the authentication Blueprint
    from app.auth.routes import auth

    # Register the authentication Blueprint with the Flask application
    app.register_blueprint(auth)

    # Return the configured Flask application
    return app