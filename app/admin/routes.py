# Import Blueprint, render_template and abort
from flask import Blueprint, render_template, abort

# Import login_required and current_user
from flask_login import login_required, current_user


# Create Admin Blueprint
admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# Admin Dashboard
@admin.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "admin":
        abort(403)

    return render_template("admin/dashboard.html")