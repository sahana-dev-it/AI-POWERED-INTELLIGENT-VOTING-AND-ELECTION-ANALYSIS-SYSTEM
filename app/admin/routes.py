# Import Blueprint
from flask import Blueprint

# Import login_required
from flask_login import login_required


# Create Admin Blueprint
admin = Blueprint("admin", __name__, url_prefix="/admin")


# Admin Dashboard
@admin.route("/dashboard")
@login_required
def dashboard():
    return "<h1>Admin Dashboard</h1>"