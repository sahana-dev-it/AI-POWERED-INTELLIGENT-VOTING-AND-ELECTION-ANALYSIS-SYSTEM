# Import the application factory function
from app import create_app


# Create the Flask application
app = create_app()


# Run the application only when this file is executed directly
if __name__ == "__main__":
    # Start the Flask development server
    app.run(debug=True)