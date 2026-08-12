# Import Blueprint, render_template and abort
from flask import Blueprint, render_template, abort

# Import login_required and current_user
from flask_login import login_required, current_user

# Import datetime
from datetime import datetime

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
    # Election Statistics
    # ----------------------------------

    total_elections = Election.query.count()


    # ----------------------------------
    # Calculate Active Elections
    # ----------------------------------
    # An election is active only when
    # the current date/time is between
    # its start and end date/time.
    # ----------------------------------

    current_datetime = datetime.now()

    active_elections = 0


    for election in Election.query.all():

        try:

            # Combine date and time strings
            # into one datetime object

            start_datetime = datetime.strptime(
                f"{election.start_date} {election.start_time}",
                "%Y-%m-%d %H:%M"
            )

            end_datetime = datetime.strptime(
                f"{election.end_date} {election.end_time}",
                "%Y-%m-%d %H:%M"
            )


            # ----------------------------------
            # Check whether election is active
            # ----------------------------------

            if (
                start_datetime <= current_datetime
                and
                current_datetime < end_datetime
            ):

                active_elections += 1


        except (ValueError, TypeError):

            # Ignore elections with invalid
            # date/time values

            continue


    # ----------------------------------
    # Candidate and Vote Statistics
    # ----------------------------------
    # If there are no elections, these
    # statistics should not display old
    # candidate/vote records.
    # ----------------------------------

    if total_elections > 0:

        total_candidates = Candidate.query.count()

        total_votes = Vote.query.count()

    else:

        total_candidates = None

        total_votes = None


    # ----------------------------------
    # Registered Voters
    # ----------------------------------

    total_voters = User.query.filter_by(
        role="voter"
    ).count()


    # ----------------------------------
    # Calculate Voter Turnout
    # ----------------------------------

    if (
        total_voters > 0
        and
        total_votes is not None
    ):

        voter_turnout = round(
            (total_votes / total_voters) * 100,
            2
        )

    else:

        voter_turnout = 0


    # ----------------------------------
    # Send Statistics to Dashboard
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