# Import Flask tools
from flask import Blueprint, render_template, redirect, flash

# Import Flask-Login
from flask_login import login_required, current_user

# Import database
from app import db

# Import models
from app.models.election import Election
from app.models.candidate import Candidate
from app.models.vote import Vote

# Import datetime
from datetime import datetime


# ----------------------------------
# Create Results Blueprint
# ----------------------------------

results = Blueprint(
    "results",
    __name__,
    url_prefix="/results"
)


# ----------------------------------
# Function to update election status
# ----------------------------------

def update_election_status(election):

    try:

        # Convert stored date and time
        # into Python datetime objects

        start_datetime = datetime.strptime(
            f"{election.start_date} {election.start_time}",
            "%Y-%m-%d %H:%M"
        )

        end_datetime = datetime.strptime(
            f"{election.end_date} {election.end_time}",
            "%Y-%m-%d %H:%M"
        )

        # Current date and time
        current_datetime = datetime.now()

        # ----------------------------------
        # Upcoming
        # ----------------------------------

        if current_datetime < start_datetime:

            election.status = "Upcoming"

        # ----------------------------------
        # Active
        # ----------------------------------

        elif (
            current_datetime >= start_datetime
            and
            current_datetime < end_datetime
        ):

            election.status = "Active"

        # ----------------------------------
        # Completed
        # ----------------------------------

        else:

            election.status = "Completed"

    except (ValueError, TypeError):

        pass


# ----------------------------------
# Results Page
# ----------------------------------

@results.route("/<int:election_id>")
@login_required
def view_results(election_id):

    # ----------------------------------
    # Check Admin
    # ----------------------------------

    if current_user.role != "admin":

        flash(
            "Only administrators can view election results.",
            "danger"
        )

        return redirect("/voter/dashboard")


    # ----------------------------------
    # Find Election
    # ----------------------------------

    election = Election.query.get_or_404(
        election_id
    )


    # ----------------------------------
    # Update Election Status
    # ----------------------------------

    update_election_status(election)

    db.session.commit()


    # ----------------------------------
    # Results only after election ends
    # ----------------------------------

    if election.status != "Completed":

        if election.status == "Upcoming":

            flash(
                "Results are not available because the election has not started yet.",
                "warning"
            )

        elif election.status == "Active":

            flash(
                "Results will be available after the election ends.",
                "warning"
            )

        return redirect("/results/list")


    # ----------------------------------
    # Get Candidates
    # ----------------------------------

    candidates = Candidate.query.filter_by(
        election_id=election.id
    ).all()


    # ----------------------------------
    # Calculate Vote Counts
    # ----------------------------------

    results_data = []

    for candidate in candidates:

        vote_count = Vote.query.filter_by(
            election_id=election.id,
            candidate_id=candidate.id
        ).count()

        results_data.append({

            "candidate": candidate,

            "vote_count": vote_count

        })


    # ----------------------------------
    # Find Winner
    # ----------------------------------

    winner = None

    if results_data:

        highest_votes = max(
            result["vote_count"]
            for result in results_data
        )

        # Only declare winner if
        # at least one vote exists

        if highest_votes > 0:

            winners = [

                result
                for result in results_data

                if result["vote_count"]
                == highest_votes

            ]

            # If exactly one candidate
            # has the highest votes

            if len(winners) == 1:

                winner = winners[0]


    # ----------------------------------
    # Total Votes
    # ----------------------------------

    total_votes = Vote.query.filter_by(
        election_id=election.id
    ).count()


    # ----------------------------------
    # Display Results
    # ----------------------------------

    return render_template(
        "results/view.html",

        election=election,

        results=results_data,

        winner=winner,

        total_votes=total_votes
    )


# ----------------------------------
# List Completed Elections
# ----------------------------------

@results.route("/list")
@login_required
def list_results():

    # ----------------------------------
    # Check Admin
    # ----------------------------------

    if current_user.role != "admin":

        flash(
            "Only administrators can view election results.",
            "danger"
        )

        return redirect("/voter/dashboard")


    # ----------------------------------
    # Get all elections
    # ----------------------------------

    elections = Election.query.all()


    # ----------------------------------
    # Update statuses
    # ----------------------------------

    for election in elections:

        update_election_status(election)


    db.session.commit()


    # ----------------------------------
    # Only completed elections
    # ----------------------------------

    completed_elections = [

        election

        for election in elections

        if election.status == "Completed"

    ]


    # ----------------------------------
    # Display completed elections
    # ----------------------------------

    return render_template(
        "results/list.html",

        elections=completed_elections
    )