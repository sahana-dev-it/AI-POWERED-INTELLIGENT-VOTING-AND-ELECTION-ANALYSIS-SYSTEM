# Import Blueprint and render_template from Flask
from flask import Blueprint, render_template, request


# Create a Blueprint for authentication-related routes
auth = Blueprint("auth", __name__)


# Registration route
@auth.route("/register", methods=["GET", "POST"])
def register():

    # Check if the form was submitted
    if request.method == "POST":

        # Get data from the registration form
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Temporarily print the data in the terminal
        print("Name:", name)
        print("Email:", email)
        print("Password:", password)

        return "Registration form submitted successfully!"

    # Display the registration page
    return render_template("register.html")