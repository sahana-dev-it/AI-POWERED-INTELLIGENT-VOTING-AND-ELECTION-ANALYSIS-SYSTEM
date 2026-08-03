# Import the Flask class from the Flask framework
from flask import Flask

# Import SQLAlchemy to connect Flask with our database
from flask_sqlalchemy import SQLAlchemy

# Import LoginManager to manage user login sessions
from flask_login import LoginManager

# Import Flask-Mail
from flask_mail import Mail

# Import operating system tools
import os

# Import dotenv
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()


# --------------------------------------------------
# CREATE EXTENSION OBJECTS
# --------------------------------------------------

# Create the database object
db = SQLAlchemy()

# Create the mail object
mail = Mail()

# Create the login manager object
login_manager = LoginManager()

# Set the login page
login_manager.login_view = "auth.login"


# --------------------------------------------------
# FLASK-LOGIN USER LOADER
# --------------------------------------------------

@login_manager.user_loader
def load_user(user_id):

    from app.models.user import User

    return User.query.get(int(user_id))


# --------------------------------------------------
# CREATE FLASK APPLICATION
# --------------------------------------------------

def create_app():

    # Create Flask application
    #
    # Our CSS is inside:
    # app/static/css/style.css
    #
    # Therefore Flask will use app/static
    # as its static folder.
    app = Flask(
        __name__,
        static_folder="static",
        static_url_path="/static"
    )


    # --------------------------------------------------
    # GMAIL CONFIGURATION
    # --------------------------------------------------

    app.config["MAIL_SERVER"] = "smtp.gmail.com"

    app.config["MAIL_PORT"] = 587

    app.config["MAIL_USE_TLS"] = True

    app.config["MAIL_USERNAME"] = os.getenv(
        "MAIL_USERNAME"
    )

    app.config["MAIL_PASSWORD"] = os.getenv(
        "MAIL_PASSWORD"
    )

    app.config["MAIL_DEFAULT_SENDER"] = os.getenv(
        "MAIL_USERNAME"
    )


    # --------------------------------------------------
    # SECRET KEY
    # --------------------------------------------------

    app.config["SECRET_KEY"] = "VotingSystem@2026"


    # --------------------------------------------------
    # DATABASE CONFIGURATION
    # --------------------------------------------------

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///../database/voting_system.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    # --------------------------------------------------
    # INITIALIZE DATABASE
    # --------------------------------------------------

    db.init_app(app)


    # --------------------------------------------------
    # INITIALIZE LOGIN MANAGER
    # --------------------------------------------------

    login_manager.init_app(app)


    # --------------------------------------------------
    # INITIALIZE MAIL
    # --------------------------------------------------

    mail.init_app(app)


    # --------------------------------------------------
    # IMPORT MODELS
    # --------------------------------------------------

    from app.models.user import User
    from app.models.election import Election
    from app.models.candidate import Candidate
    from app.models.vote import Vote


    # --------------------------------------------------
    # MAIN BLUEPRINT
    # --------------------------------------------------

    from app.routes import main

    app.register_blueprint(main)


    # --------------------------------------------------
    # AUTHENTICATION BLUEPRINT
    # --------------------------------------------------

    from app.auth.routes import auth

    app.register_blueprint(auth)


    # --------------------------------------------------
    # ADMIN BLUEPRINT
    # --------------------------------------------------

    from app.admin.routes import admin

    app.register_blueprint(admin)


    # --------------------------------------------------
    # VOTER BLUEPRINT
    # --------------------------------------------------

    from app.voter.routes import voter

    app.register_blueprint(voter)


    # --------------------------------------------------
    # ELECTION BLUEPRINT
    # --------------------------------------------------

    from app.election.routes import election

    app.register_blueprint(election)


    # --------------------------------------------------
    # CANDIDATE BLUEPRINT
    # --------------------------------------------------

    from app.candidate.routes import candidate

    app.register_blueprint(candidate)


    # --------------------------------------------------
    # VOTE BLUEPRINT
    # --------------------------------------------------

    from app.vote.routes import vote

    app.register_blueprint(vote)


    # --------------------------------------------------
    # RESULTS BLUEPRINT
    # --------------------------------------------------

    from app.results.routes import results

    app.register_blueprint(results)


    # --------------------------------------------------
    # CREATE DATABASE TABLES
    # --------------------------------------------------

    with app.app_context():

        db.create_all()


    # --------------------------------------------------
    # RETURN APPLICATION
    # --------------------------------------------------

    return app