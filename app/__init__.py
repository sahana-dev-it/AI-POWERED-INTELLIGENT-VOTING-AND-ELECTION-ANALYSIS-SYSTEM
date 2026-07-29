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


# Tell Flask-Login how to load a user from the database
@login_manager.user_loader
def load_user(user_id):

    # Import the User model
    from app.models.user import User

    # Find and return the user using their ID
    return User.query.get(int(user_id))


# This function creates and configures our Flask application
def create_app():

    # Create a Flask application instance
    app = Flask(__name__)

    # Secret key used to secure user sessions
    app.config["SECRET_KEY"] = "VotingSystem@2026"

    # Display template folder information (for debugging)
    print("Flask template folder:", app.template_folder)
    print("Flask template path:", app.jinja_loader.searchpath)

    # Configure the SQLite database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/voting_system.db"

    # Disable unnecessary modification tracking
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Connect the database object to our Flask application
    db.init_app(app)

    # Connect Flask-Login to our Flask application
    login_manager.init_app(app)

    # Import the User model so SQLAlchemy knows about the User table
    from app.models.user import User
    from app.election.models import Election

    # Import the main Blueprint
    from app.routes import main

    # Register the main Blueprint
    app.register_blueprint(main)

    # Import the authentication Blueprint
    from app.auth.routes import auth

    # Register the authentication Blueprint
    app.register_blueprint(auth)

    # Import the Admin Blueprint
    from app.admin.routes import admin

    # Register the Admin Blueprint
    app.register_blueprint(admin)

    # Import the Voter Blueprint
    from app.voter.routes import voter

    # Register the Voter Blueprint
    app.register_blueprint(voter)

    # Return the configured Flask application
    return app