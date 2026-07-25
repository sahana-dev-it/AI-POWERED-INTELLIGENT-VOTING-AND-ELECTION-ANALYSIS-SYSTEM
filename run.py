# Import the Flask class from the flask package
from flask import Flask

# Create the Flask application
app = Flask(__name__)


# This route handles the home page of our application
@app.route("/")
def home():
    # Return a simple message to test whether Flask is working
    return "AI-Powered Intelligent Voting and Election Analysis System"


# This block runs the application when we execute: python run.py
if __name__ == "__main__":
    # Start the Flask development server
    app.run(debug=True)