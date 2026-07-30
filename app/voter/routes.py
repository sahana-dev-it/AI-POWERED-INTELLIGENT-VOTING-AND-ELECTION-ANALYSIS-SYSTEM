# Import Blueprint and render_template
from flask import Blueprint, render_template

# Import login_required
from flask_login import login_required


# Create Voter Blueprint
voter = Blueprint(
    "voter",
    __name__,
    url_prefix="/voter"
)


# Voter Dashboard
@voter.route("/dashboard")
@login_required
def dashboard():

    return render_template("voter/dashboard.html")