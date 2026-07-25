# Import Blueprint from Flask
from flask import Blueprint


# Create a Blueprint for the main application routes
main = Blueprint("main", __name__)


# Define the home page route
@main.route("/")
def home():
    # Return the project title to confirm that the application is working
    return "AI-Powered Intelligent Voting and Election Analysis System"