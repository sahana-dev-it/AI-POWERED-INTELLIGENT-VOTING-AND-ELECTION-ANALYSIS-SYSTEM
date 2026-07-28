# Import the database object
from app import db

# Import UserMixin for Flask-Login
from flask_login import UserMixin


# Create the User database model
class User(UserMixin, db.Model):

    # Create a unique ID for every user
    id = db.Column(db.Integer, primary_key=True)

    # Store the user's full name
    name = db.Column(db.String(100), nullable=False)

    # Store the user's email address
    # unique=True means two users cannot use the same email
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Store the user's password
    # We will later store a securely hashed password here
    password = db.Column(db.String(200), nullable=False)

    # Store the user's role
    # A user can be either a voter or an admin
    role = db.Column(db.String(20), nullable=False, default="voter")