# Import Flask tools
from flask import Blueprint, render_template, request, redirect, url_for, session

# Import Flask-Login
from flask_login import login_user

# Import password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# Import SQLAlchemy IntegrityError
from sqlalchemy.exc import IntegrityError

# Import database and User model
from app import db
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

            db.session.add(new_user)

            db.session.commit()


            # ----------------------------------
            # Store email temporarily in session
            # ----------------------------------

            session["verification_email"] = email


            # ----------------------------------
            # TEMPORARY TESTING
            # ----------------------------------

            print("")
            print("====================================")
            print("EMAIL VERIFICATION OTP")
            print("Email:", email)
            print("OTP:", verification_code)
            print("====================================")
            print("")


            # Redirect to OTP page
            return redirect(
                url_for("auth.verify_otp")
            )


        except IntegrityError:

            db.session.rollback()

            message = (
                "This email is already registered."
            )


    return render_template(
        "register.html",
        message=message
    )


# ----------------------------------
# OTP Verification
# ----------------------------------

@auth.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    email = session.get(
        "verification_email"
    )


    # If there is no email in session
    if not email:

        return redirect(
            url_for("auth.register")
        )


    user = User.query.filter_by(
        email=email
    ).first()


    if not user:

        session.pop(
            "verification_email",
            None
        )

        return redirect(
            url_for("auth.register")
        )


    message = ""


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
            datetime.utcnow()
            <= user.verification_expiry
        ):

            # Mark email as verified
            user.email_verified = True

            # Remove OTP
            user.verification_code = None

            user.verification_expiry = None


            db.session.commit()


            # Remove temporary session
            session.pop(
                "verification_email",
                None
            )


            return render_template(
                "verification_success.html"
            )


        else:

            message = (
                "Invalid or expired OTP."
            )


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

        email = request.form[
            "email"
        ].strip().lower()

        password = request.form[
            "password"
        ]


        # Find user
        user = User.query.filter_by(
            email=email
        ).first()


        if user:

            # Check password
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


                # Login user
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


        # Invalid login
        message = (
            "Invalid email or password."
        )


    return render_template(
        "login.html",
        message=message
    )