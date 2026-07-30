# Import the Flask class from the Flask framework
from flask import Flask

# Import SQLAlchemy to connect Flask with our database
from flask_sqlalchemy import SQLAlchemy

# Import LoginManager to manage user login sessions
from flask_login import LoginManager


# Create the database object
db = SQLAlchemy()


# Create the login manager object
login_manager = LoginManager()

# Set the login page
login_manager.login_view = "auth.login"


# Tell Flask-Login how to load a user
@login_manager.user_loader
def load_user(user_id):

    from app.models.user import User

    return User.query.get(int(user_id))


# Create Flask application
def create_app():

    app = Flask(__name__)

    # Secret key
    app.config["SECRET_KEY"] = "VotingSystem@2026"

    # SQLite Database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/voting_system.db"

    # Disable modification tracking
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    db.init_app(app)

    # Initialize Login Manager
    login_manager.init_app(app)

    # Import Models
    # Import Models
    from app.models.user import User
    from app.models.election import Election
    from app.models.candidate import Candidate
    from app.models.vote import Vote

    # Import Main Blueprint
    from app.routes import main
    app.register_blueprint(main)

    # Import Authentication Blueprint
    from app.auth.routes import auth
    app.register_blueprint(auth)

    # Import Admin Blueprint
    from app.admin.routes import admin
    app.register_blueprint(admin)

    # Import Voter Blueprint
    from app.voter.routes import voter
    app.register_blueprint(voter)

    # Import Election Blueprint
    from app.election.routes import election
    app.register_blueprint(election)

    # Import Candidate Blueprint
    from app.candidate.routes import candidate
    app.register_blueprint(candidate)
    # Import Vote Blueprint
    from app.vote.routes import vote

    # Register Vote Blueprint
    app.register_blueprint(vote)
    # Create all database tables
    with app.app_context():
        db.create_all()

    return app