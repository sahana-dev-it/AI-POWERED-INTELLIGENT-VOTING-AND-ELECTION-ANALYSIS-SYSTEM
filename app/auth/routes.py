from flask_login import login_user
# Import Blueprint, render_template and request from Flask
from flask import Blueprint, render_template, request, redirect, url_for

# Import password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# Import SQLAlchemy IntegrityError
from sqlalchemy.exc import IntegrityError

# Import database and User model
from app import db
from app.models.user import User


# Authentication Blueprint
auth = Blueprint("auth", __name__)


# Registration Page
@auth.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        # Get form data
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create new user
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            role="voter"
        )

        try:

            db.session.add(new_user)
            db.session.commit()

            message = "Registration Successful!"

        except IntegrityError:

            db.session.rollback()

            message = "This email is already registered."

    return render_template("register.html", message=message)
# Login route
# GET  -> Display the login page
# POST -> Check email and password
@auth.route("/login", methods=["GET", "POST"])
# Login route
# GET  -> Display the login page
# POST -> Check email and password
@auth.route("/login", methods=["GET", "POST"])
def login():

    # Variable to store success/error messages
    message = ""

    # Check if the user submitted the login form
    if request.method == "POST":

        # Get email and password entered by the user
        email = request.form["email"]
        password = request.form["password"]

        # Search for the user in the database using email
        user = User.query.filter_by(email=email).first()

        # Check whether the user exists
        if user:

            # Verify the entered password with the hashed password
            if check_password_hash(user.password, password):

                # Log the user in
                login_user(user)

                # Check whether the logged-in user is an Admin
                if user.role == "admin":
                    return redirect(url_for("admin.dashboard"))

                # Otherwise, the user is a Voter
                return redirect(url_for("voter.dashboard"))

        # If email or password is incorrect
        message = "Invalid email or password."

    # Display the login page
    return render_template("login.html", message=message)