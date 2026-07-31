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
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    # Store the user's securely hashed password
    password = db.Column(
        db.String(200),
        nullable=False
    )

    # Store the user's role
    # A user can be either a voter or an admin
    role = db.Column(
        db.String(20),
        nullable=False,
        default="voter"
    )

    # ----------------------------------
    # Email Verification
    # ----------------------------------

    # Whether the user's email has been verified
    email_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    # Temporary OTP verification code
    verification_code = db.Column(
        db.String(10),
        nullable=True
    )

    # Time until which the OTP is valid
    verification_expiry = db.Column(
        db.DateTime,
        nullable=True
    )