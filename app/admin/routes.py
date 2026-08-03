# Import Blueprint, render_template and abort
from flask import Blueprint, render_template, abort

# Import login_required and current_user
from flask_login import login_required, current_user

# Import database
from app import db

# Import models
from app.models.election import Election
from app.models.candidate import Candidate
from app.models.vote import Vote
from app.models.user import User


# ----------------------------------
# Create Admin Blueprint
# ----------------------------------

admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# ----------------------------------
# Admin Dashboard
# ----------------------------------

@admin.route("/dashboard")
@login_required
def dashboard():

    # ----------------------------------
    # Only Admin can access dashboard
    # ----------------------------------

    if current_user.role != "admin":
        abort(403)


    # ----------------------------------
    # Basic Statistics
    # ----------------------------------

    total_elections = Election.query.count()

    active_elections = Election.query.filter_by(
        status="Active"
    ).count()

    total_candidates = Candidate.query.count()

    total_votes = Vote.query.count()

    total_voters = User.query.filter_by(
        role="voter"
    ).count()


    # ----------------------------------
    # Calculate Voter Turnout
    # ----------------------------------

    if total_voters > 0:

        voter_turnout = round(
            (total_votes / total_voters) * 100,
            2
        )

    else:

        voter_turnout = 0


    # ----------------------------------
    # Send statistics to dashboard
    # ----------------------------------

    return render_template(
        "admin/dashboard.html",

        total_elections=total_elections,

        active_elections=active_elections,

        total_candidates=total_candidates,

        total_votes=total_votes,

        total_voters=total_voters,

        voter_turnout=voter_turnout
    )