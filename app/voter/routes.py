# Import Blueprint
from flask import Blueprint

# Import login_required
from flask_login import login_required


# Create Voter Blueprint
voter = Blueprint("voter", __name__, url_prefix="/voter")


# Voter Dashboard
@voter.route("/dashboard")
@login_required
def dashboard():
    return "<h1>Voter Dashboard</h1>"