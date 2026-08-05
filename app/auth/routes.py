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


# ==========================================
# AUTHENTICATION BLUEPRINT
# ==========================================

auth = Blueprint("auth", __name__)


# ==========================================
# REGISTRATION
# ==========================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        # ----------------------------------
        # Get form data
        # ----------------------------------

        name = request.form.get("name", "").strip()

        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get(
            "password", ""
        )

        confirm_password = request.form.get(
            "confirm_password", ""
        )


        # ----------------------------------
        # Check required fields
        # ----------------------------------

        if not name or not email or not password:

            message = "Please fill in all required fields."

            return render_template(
                "register.html",
                message=message
            )


        # ----------------------------------
        # Check password confirmation
        # ----------------------------------

        if password != confirm_password:

            message = "Passwords do not match."

            return render_template(
                "register.html",
                message=message
            )


        # ----------------------------------
        # Check password requirements
        # ----------------------------------

        if (
            len(password) < 8
            or not any(c.isupper() for c in password)
            or not any(c.islower() for c in password)
            or not any(c.isdigit() for c in password)
        ):

            message = (
                "Password must contain at least 8 characters, "
                "one uppercase letter, one lowercase letter "
                "and one number."
            )

            return render_template(
                "register.html",
                message=message
            )


        # ----------------------------------
        # Check existing email
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
        # Generate password hash
        # ----------------------------------

        hashed_password = generate_password_hash(
            password
        )


        # ==================================
        # GENERATE OTP
        # ==================================

        verification_code = str(
            random.randint(100000, 999999)
        )


        # OTP valid for 10 minutes
        verification_expiry = (
            datetime.utcnow()
            + timedelta(minutes=10)
        )


        # ----------------------------------
        # Create voter
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

            # ----------------------------------
            # Save user
            # ----------------------------------

            db.session.add(new_user)

            db.session.commit()


            # ==================================
            # SEND OTP EMAIL
            # ==================================

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
            # Store email in session
            # ----------------------------------

            session["verification_email"] = email


            # ----------------------------------
            # Redirect to OTP page
            # ----------------------------------

            return redirect(
                url_for("auth.verify_otp")
            )


        except IntegrityError:

            db.session.rollback()

            message = (
                "This email is already registered."
            )


        except Exception as e:

            db.session.rollback()

            print(
                "EMAIL ERROR:",
                repr(e)
            )

            message = (
                "Unable to send verification email. "
                "Please check your email configuration "
                "and try again."
            )


    return render_template(
        "register.html",
        message=message
    )


# ==========================================
# OTP VERIFICATION
# ==========================================

@auth.route(
    "/verify-otp",
    methods=["GET", "POST"]
)
def verify_otp():

    # ----------------------------------
    # Get email from session
    # ----------------------------------

    email = session.get(
        "verification_email"
    )


    # If email is not available
    if not email:

        return redirect(
            url_for("auth.register")
        )


    # ----------------------------------
    # Find user
    # ----------------------------------

    user = User.query.filter_by(
        email=email
    ).first()


    # If user does not exist
    if not user:

        session.pop(
            "verification_email",
            None
        )

        return redirect(
            url_for("auth.register")
        )


    # ----------------------------------
    # If already verified
    # ----------------------------------

    if user.email_verified:

        session.pop(
            "verification_email",
            None
        )

        return redirect(
            url_for("auth.login")
        )


    message = ""


    # ==================================
    # VERIFY OTP
    # ==================================

    if request.method == "POST":

        entered_code = request.form.get(
            "verification_code",
            ""
        ).strip()


        # ----------------------------------
        # Check OTP format
        # ----------------------------------

        if (
            not entered_code.isdigit()
            or len(entered_code) != 6
        ):

            message = (
                "Please enter the 6-digit OTP."
            )

            return render_template(
                "verify_otp.html",
                message=message,
                email=email
            )


        # ----------------------------------
        # Check stored OTP
        # ----------------------------------

        stored_code = (
            str(user.verification_code).strip()
            if user.verification_code
            else ""
        )


        # ----------------------------------
        # Check expiry
        # ----------------------------------

        current_time = datetime.utcnow()


        if not user.verification_expiry:

            message = (
                "This OTP has expired. "
                "Please register again."
            )

            return render_template(
                "verify_otp.html",
                message=message,
                email=email
            )


        # ==================================
        # VALID OTP
        # ==================================

        if (
            stored_code == entered_code
            and
            current_time <= user.verification_expiry
        ):

            # Mark email verified
            user.email_verified = True


            # Remove OTP
            user.verification_code = None


            # Remove expiry
            user.verification_expiry = None


            # Save changes
            db.session.commit()


            # Remove session email
            session.pop(
                "verification_email",
                None
            )


            # ----------------------------------
            # Success page
            # ----------------------------------

            return render_template(
                "verification_success.html"
            )


        # ==================================
        # INVALID / EXPIRED OTP
        # ==================================

        if stored_code != entered_code:

            message = (
                "Invalid OTP. Please enter the "
                "6-digit code sent to your email."
            )

        elif current_time > user.verification_expiry:

            message = (
                "This OTP has expired. "
                "Please register again."
            )


    # ----------------------------------
    # Display OTP page
    # ----------------------------------

    return render_template(
        "verify_otp.html",
        message=message,
        email=email
    )


# ==========================================
# LOGIN
# ==========================================

@auth.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    message = ""


    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()


        password = request.form.get(
            "password",
            ""
        )


        # ----------------------------------
        # Find user
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
                        "Please verify your email "
                        "before logging in."
                    )

                    return render_template(
                        "login.html",
                        message=message
                    )


                # ----------------------------------
                # Login user
                # ----------------------------------

                login_user(user)


                # ----------------------------------
                # Admin
                # ----------------------------------

                if user.role == "admin":

                    return redirect(
                        url_for(
                            "admin.dashboard"
                        )
                    )


                # ----------------------------------
                # Voter
                # ----------------------------------

                return redirect(
                    url_for(
                        "voter.dashboard"
                    )
                )


        # ----------------------------------
        # Invalid login
        # ----------------------------------

        message = (
            "Invalid email or password."
        )


    return render_template(
        "login.html",
        message=message
    )
# ==========================================
# LOGOUT
# ==========================================

@auth.route("/logout")
def logout():

    from flask_login import logout_user

    # Log out the current user
    logout_user()

    # Return to login page
    return redirect(
        url_for("auth.login")
    )