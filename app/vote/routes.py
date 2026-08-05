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


# ==========================================
# Create Vote Blueprint
# ==========================================

vote = Blueprint(
    "vote",
    __name__,
    url_prefix="/vote"
)


# ==========================================
# Function to update election status
# ==========================================

def update_election_status(election):

    try:

        start_datetime = datetime.strptime(
            f"{election.start_date} {election.start_time}",
            "%Y-%m-%d %H:%M"
        )

        end_datetime = datetime.strptime(
            f"{election.end_date} {election.end_time}",
            "%Y-%m-%d %H:%M"
        )

        current_datetime = datetime.now()

        # Election has not started
        if current_datetime < start_datetime:

            election.status = "Upcoming"

        # Election is active
        elif (
            current_datetime >= start_datetime
            and
            current_datetime < end_datetime
        ):

            election.status = "Active"

        # Election has ended
        else:

            election.status = "Completed"

    except (ValueError, TypeError):

        pass


# ==========================================
# Show Active Elections
# ==========================================

@vote.route("/elections")
@login_required
def elections():

    # Get all elections
    all_elections = Election.query.all()

    # Update status
    for election in all_elections:

        update_election_status(election)

    # Save updated statuses
    db.session.commit()

    # Get only active elections
    elections = Election.query.filter_by(
        status="Active"
    ).all()

    return render_template(
        "vote/elections.html",
        elections=elections
    )


# ==========================================
# Show Candidates
# ==========================================

@vote.route("/candidates/<int:election_id>")
@login_required
def candidates(election_id):

    # Find election
    election = Election.query.get_or_404(
        election_id
    )

    # Update election status
    update_election_status(election)

    db.session.commit()

    # Prevent voting if election is not active
    if election.status != "Active":

        if election.status == "Upcoming":

            flash(
                "This election has not started yet.",
                "warning"
            )

        elif election.status == "Completed":

            flash(
                "This election has already ended.",
                "warning"
            )

        return redirect(
            "/vote/elections"
        )

    # Get candidates
    candidates = Candidate.query.filter_by(
        election_id=election_id
    ).all()

    # Check whether voter already voted
    existing_vote = Vote.query.filter_by(
        voter_id=current_user.id,
        election_id=election.id
    ).first()

    return render_template(
        "vote/candidates.html",
        election=election,
        candidates=candidates,
        has_voted=existing_vote is not None
    )


# ==========================================
# Cast Vote
# ==========================================

@vote.route(
    "/cast/<int:election_id>/<int:candidate_id>",
    methods=["POST"]
)
@login_required
def cast_vote(election_id, candidate_id):

    # --------------------------------------
    # Find election
    # --------------------------------------

    election = Election.query.get_or_404(
        election_id
    )

    # --------------------------------------
    # Update election status
    # --------------------------------------

    update_election_status(election)

    db.session.commit()

    # --------------------------------------
    # Check election status
    # --------------------------------------

    if election.status != "Active":

        if election.status == "Upcoming":

            flash(
                "Voting has not started yet.",
                "warning"
            )

        elif election.status == "Completed":

            flash(
                "Voting for this election has ended.",
                "warning"
            )

        return redirect(
            f"/vote/candidates/{election.id}"
        )

    # --------------------------------------
    # Find candidate
    # --------------------------------------

    candidate = Candidate.query.get_or_404(
        candidate_id
    )

    # --------------------------------------
    # Make sure candidate belongs
    # to this election
    # --------------------------------------

    if candidate.election_id != election.id:

        flash(
            "Invalid candidate for this election.",
            "danger"
        )

        return redirect(
            "/vote/elections"
        )

    # --------------------------------------
    # Check whether voter already voted
    # --------------------------------------

    existing_vote = Vote.query.filter_by(
        voter_id=current_user.id,
        election_id=election.id
    ).first()

    if existing_vote:

        flash(
            "You have already voted in this election.",
            "warning"
        )

        return redirect(
            f"/vote/candidates/{election.id}"
        )

    # --------------------------------------
    # Create new vote
    # --------------------------------------

    new_vote = Vote(

        voter_id=current_user.id,

        election_id=election.id,

        candidate_id=candidate.id,

        vote_time=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    # --------------------------------------
    # Save vote
    # --------------------------------------

    db.session.add(new_vote)

    db.session.commit()

    # --------------------------------------
    # Redirect to success page
    # --------------------------------------

    return render_template(
        "vote/vote_success.html",
        election=election,
        candidate=candidate
    )