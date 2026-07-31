# Import Flask tools
from flask import Blueprint, render_template, request, redirect, url_for, session

# Import Flask-Login
from flask_login import login_user

# Import password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# Import SQLAlchemy IntegrityError
from sqlalchemy.exc import IntegrityError

# Import Flask-Mail
from flask_mail import Message

# Import database and User model
from app import db, mail
from app.models.user import User

# Import OTP tools
import random
from datetime import datetime, timedelta


# ----------------------------------
# Authentication Blueprint
# ----------------------------------

auth = Blueprint("auth", __name__)


# ----------------------------------
# Registration
# ----------------------------------

@auth.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        # Get form data
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        # ----------------------------------
        # Check whether email already exists
        # ----------------------------------

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            message = "This email is already registered."

            return render_template(
                "register.html",
                message=message
            )

        # ----------------------------------
        # Create password hash
        # ----------------------------------

        hashed_password = generate_password_hash(
            password
        )

        # ----------------------------------
        # Generate 6-digit OTP
        # ----------------------------------

        verification_code = str(
            random.randint(100000, 999999)
        )

        # OTP valid for 10 minutes
        verification_expiry = (
            datetime.utcnow() + timedelta(minutes=10)
        )

        # ----------------------------------
        # Create new voter
        # ----------------------------------

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            role="voter",
            email_verified=False,
            verification_code=verification_code,
            verification_expiry=verification_expiry
        )

        try:

            # Add user to database
            db.session.add(new_user)

            # Save user
            db.session.commit()

            # ----------------------------------
            # Send OTP to user's email
            # ----------------------------------

            msg = Message(
    subject="Voting System - Email Verification OTP",
    recipients=[email]
)

            msg.body = f"""
Hello {name},

Thank you for registering with the
AI-Powered Intelligent Voting and Election Analysis System.

Your email verification OTP is:

{verification_code}

This OTP is valid for 10 minutes.

Please do not share this OTP with anyone.

Regards,
Voting System
"""

            # Send email
            mail.send(msg)

            # ----------------------------------
            # Store email temporarily in session
            # ----------------------------------

            session["verification_email"] = email

            # ----------------------------------
            # Redirect to OTP page
            # ----------------------------------

            return redirect(
                url_for("auth.verify_otp")
            )

        except IntegrityError:

            # Undo database changes
            db.session.rollback()

            message = "This email is already registered."

        except Exception as e:

            # Undo database changes if email sending fails
            db.session.rollback()

            print("EMAIL ERROR:", e)

            message = (
                "Unable to send verification email. "
                "Please try again."
            )

    # Display registration page
    return render_template(
        "register.html",
        message=message
    )


# ----------------------------------
# OTP Verification
# ----------------------------------

@auth.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    # Get email stored during registration
    email = session.get(
        "verification_email"
    )

    # If there is no email in session
    if not email:

        return redirect(
            url_for("auth.register")
        )

    # Find user
    user = User.query.filter_by(
        email=email
    ).first()

    # If user doesn't exist
    if not user:

        session.pop(
            "verification_email",
            None
        )

        return redirect(
            url_for("auth.register")
        )

    message = ""

    # ----------------------------------
    # Verify OTP
    # ----------------------------------

    if request.method == "POST":

        entered_code = request.form[
            "verification_code"
        ].strip()

        # ----------------------------------
        # Check OTP
        # ----------------------------------

        if (
            user.verification_code == entered_code
            and
            user.verification_expiry
            and
            datetime.utcnow() <= user.verification_expiry
        ):

            # Mark email as verified
            user.email_verified = True

            # Remove OTP
            user.verification_code = None

            # Remove OTP expiry
            user.verification_expiry = None

            # Save changes
            db.session.commit()

            # Remove temporary session
            session.pop(
                "verification_email",
                None
            )

            # Show success page
            return render_template(
                "verification_success.html"
            )

        else:

            message = (
                "Invalid or expired OTP."
            )

    # Display OTP page
    return render_template(
        "verify_otp.html",
        message=message,
        email=email
    )


# ----------------------------------
# Login
# ----------------------------------

@auth.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        # Get login details
        email = request.form[
            "email"
        ].strip().lower()

        password = request.form[
            "password"
        ]

        # ----------------------------------
        # Find user by email
        # ----------------------------------

        user = User.query.filter_by(
            email=email
        ).first()

        if user:

            # ----------------------------------
            # Check password
            # ----------------------------------

            if check_password_hash(
                user.password,
                password
            ):

                # ----------------------------------
                # Check email verification
                # ----------------------------------

                if not user.email_verified:

                    message = (
                        "Please verify your email before logging in."
                    )

                    return render_template(
                        "login.html",
                        message=message
                    )

                # ----------------------------------
                # Log user in
                # ----------------------------------

                login_user(user)

                # ----------------------------------
                # Admin
                # ----------------------------------

                if user.role == "admin":

                    return redirect(
                        url_for("admin.dashboard")
                    )

                # ----------------------------------
                # Voter
                # ----------------------------------

                return redirect(
                    url_for("voter.dashboard")
                )

        # ----------------------------------
        # Invalid login
        # ----------------------------------

        message = (
            "Invalid email or password."
        )

    # Display login page
    return render_template(
        "login.html",
        message=message
    )