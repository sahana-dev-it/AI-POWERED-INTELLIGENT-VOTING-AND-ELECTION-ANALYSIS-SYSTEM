# Import the application factory function
from app import create_app

# Import the database object
from app import db

# Create the Flask application
app = create_app()


# This block runs only when we execute: python run.py
if __name__ == "__main__":

    # Create an application context
    # This allows Flask to work with the database
    with app.app_context():

        # Create all database tables based on our models
        db.create_all()

    # Start the Flask development server
    app.run(debug=True)