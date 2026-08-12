# ==========================================
# VOTE ROUTES
# File: app/vote/routes.py
# ==========================================

from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    redirect,
    flash
)

from flask_login import login_required, current_user

from app import db

from app.models.election import Election
from app.models.candidate import Candidate
from app.models.vote import Vote


# ==========================================
# CREATE VOTE BLUEPRINT
# ==========================================

vote = Blueprint(
    "vote",
    __name__,
    url_prefix="/vote"
)


# ==========================================
# CHECK WHETHER ELECTION IS MULTIPLE POSITION
# ==========================================

def is_multiple_position_election(election):
    """
    Returns True when the election allows
    voting for multiple positions.

    Supports both possible values:
        "multiple"
        "Multiple Positions"
    """

    election_type = str(
        election.election_type or ""
    ).strip().lower()

    return election_type in (
        "multiple",
        "multiple positions"
    )


# ==========================================
# UPDATE ELECTION STATUS
# ==========================================

def update_election_status(election):

    try:

        # ----------------------------------
        # Convert start date/time
        # ----------------------------------

        if isinstance(
            election.start_date,
            datetime
        ):
            start_date = election.start_date.date()
        else:
            start_date = election.start_date

        # ----------------------------------
        # Convert end date/time
        # ----------------------------------

        if isinstance(
            election.end_date,
            datetime
        ):
            end_date = election.end_date.date()
        else:
            end_date = election.end_date

        # ----------------------------------
        # Convert time values
        # ----------------------------------

        start_time = election.start_time
        end_time = election.end_time

        # If database returns strings
        if isinstance(start_time, str):

            start_time = datetime.strptime(
                start_time[:5],
                "%H:%M"
            ).time()

        if isinstance(end_time, str):

            end_time = datetime.strptime(
                end_time[:5],
                "%H:%M"
            ).time()

        # ----------------------------------
        # Create datetime values
        # ----------------------------------

        start_datetime = datetime.combine(
            start_date,
            start_time
        )

        end_datetime = datetime.combine(
            end_date,
            end_time
        )

        current_datetime = datetime.now()

        # ----------------------------------
        # Determine status
        # ----------------------------------

        if current_datetime < start_datetime:

            election.status = "Upcoming"

        elif (
            current_datetime >= start_datetime
            and
            current_datetime < end_datetime
        ):

            election.status = "Active"

        else:

            election.status = "Completed"

    except (
        ValueError,
        TypeError,
        AttributeError
    ):

        # Do not crash the application
        pass


# ==========================================
# SHOW ACTIVE ELECTIONS
# ==========================================

@vote.route("/elections")
@login_required
def elections():

    # ----------------------------------
    # Get all elections
    # ----------------------------------

    all_elections = Election.query.all()

    # ----------------------------------
    # Update status of every election
    # ----------------------------------

    for election in all_elections:

        update_election_status(
            election
        )

    # ----------------------------------
    # Save updated statuses
    # ----------------------------------

    db.session.commit()

    # ----------------------------------
    # Get only active elections
    # ----------------------------------

    elections = Election.query.filter_by(
        status="Active"
    ).all()

    # ----------------------------------
    # Display elections
    # ----------------------------------

    return render_template(
        "vote/elections.html",
        elections=elections
    )


# ==========================================
# SHOW CANDIDATES
# ==========================================

@vote.route(
    "/candidates/<int:election_id>"
)
@login_required
def candidates(election_id):

    # ----------------------------------
    # Find election
    # ----------------------------------

    election = Election.query.get_or_404(
        election_id
    )

    # ----------------------------------
    # Update election status
    # ----------------------------------

    update_election_status(
        election
    )

    db.session.commit()

    # ----------------------------------
    # Election must be active
    # ----------------------------------

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

    # ----------------------------------
    # Get candidates ONLY for this election
    # ----------------------------------

    candidates = Candidate.query.filter_by(
        election_id=election.id
    ).order_by(
        Candidate.position,
        Candidate.id
    ).all()

    # ----------------------------------
    # Determine election type
    # ----------------------------------

    multiple_position = (
        is_multiple_position_election(
            election
        )
    )

    # ----------------------------------
    # Get votes already made by voter
    # ----------------------------------

    voter_votes = Vote.query.filter_by(
        voter_id=current_user.id,
        election_id=election.id
    ).all()

    # ----------------------------------
    # Store voted candidate IDs
    # ----------------------------------

    voted_candidate_ids = set()

    for voter_vote in voter_votes:

        voted_candidate_ids.add(
            voter_vote.candidate_id
        )

    # ----------------------------------
    # Find positions already voted for
    # ----------------------------------

    voted_positions = set()

    if multiple_position:

        for voter_vote in voter_votes:

            voted_candidate = Candidate.query.filter_by(
                id=voter_vote.candidate_id,
                election_id=election.id
            ).first()

            if (
                voted_candidate
                and
                voted_candidate.position
            ):

                voted_positions.add(
                    voted_candidate.position.strip()
                )

    # ----------------------------------
    # For single-choice election
    # ----------------------------------

    has_voted = (
        len(voter_votes) > 0
    )

    # ----------------------------------
    # Display candidate page
    # ----------------------------------

    return render_template(

        "vote/candidates.html",

        election=election,

        candidates=candidates,

        has_voted=has_voted,

        multiple_position=multiple_position,

        voted_candidate_ids=voted_candidate_ids,

        voted_positions=voted_positions
    )


# ==========================================
# CAST VOTE
# ==========================================

@vote.route(
    "/cast/<int:election_id>/<int:candidate_id>",
    methods=["POST"]
)
@login_required
def cast_vote(
    election_id,
    candidate_id
):

    # ----------------------------------
    # Find election
    # ----------------------------------

    election = Election.query.get_or_404(
        election_id
    )

    # ----------------------------------
    # Update election status
    # ----------------------------------

    update_election_status(
        election
    )

    db.session.commit()

    # ----------------------------------
    # Check election status
    # ----------------------------------

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

    # ----------------------------------
    # Find candidate
    # ----------------------------------

    candidate = Candidate.query.get_or_404(
        candidate_id
    )

    # ----------------------------------
    # Make sure candidate belongs
    # to this election
    # ----------------------------------

    if candidate.election_id != election.id:

        flash(
            "Invalid candidate for this election.",
            "danger"
        )

        return redirect(
            "/vote/elections"
        )

    # ----------------------------------
    # Determine election type
    # ----------------------------------

    multiple_position = (
        is_multiple_position_election(
            election
        )
    )

    # ==================================
    # MULTIPLE POSITION ELECTION
    # ==================================

    if multiple_position:

        # ----------------------------------
        # Candidate must have a position
        # ----------------------------------

        if not candidate.position:

            flash(
                "This candidate does not have a valid position.",
                "danger"
            )

            return redirect(
                f"/vote/candidates/{election.id}"
            )

        position = candidate.position.strip()

        # ----------------------------------
        # Check whether voter already voted
        # for THIS POSITION
        #
        # This is the important fix.
        # ----------------------------------

        existing_position_vote = (

            Vote.query

            .join(
                Candidate,
                Vote.candidate_id == Candidate.id
            )

            .filter(
                Vote.voter_id == current_user.id,

                Vote.election_id == election.id,

                Candidate.election_id == election.id,

                Candidate.position == position
            )

            .first()
        )

        # ----------------------------------
        # Already voted for this position
        # ----------------------------------

        if existing_position_vote:

            flash(
                f"You have already voted for {position}.",
                "warning"
            )

            return redirect(
                f"/vote/candidates/{election.id}"
            )

    # ==================================
    # SINGLE CHOICE ELECTION
    # ==================================

    else:

        # ----------------------------------
        # Check whether voter already voted
        # in the entire election
        # ----------------------------------

        existing_vote = Vote.query.filter_by(

            voter_id=current_user.id,

            election_id=election.id

        ).first()

        # ----------------------------------
        # Already voted
        # ----------------------------------

        if existing_vote:

            flash(
                "You have already voted in this election.",
                "warning"
            )

            return redirect(
                f"/vote/candidates/{election.id}"
            )

    # ==================================
    # CREATE NEW VOTE
    # ==================================

    new_vote = Vote(

        voter_id=current_user.id,

        election_id=election.id,

        candidate_id=candidate.id,

        vote_time=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    # ----------------------------------
    # Save vote
    # ----------------------------------

    db.session.add(
        new_vote
    )

    db.session.commit()

    # ==================================
    # MULTIPLE POSITION SUCCESS
    # ==================================

    if multiple_position:

        flash(
            f"Your vote for {candidate.position} "
            f"has been recorded successfully.",
            "success"
        )

        # ----------------------------------
        # IMPORTANT:
        # Stay on candidates page.
        #
        # User can immediately choose
        # another position.
        # ----------------------------------

        return redirect(
            f"/vote/candidates/{election.id}"
        )

    # ==================================
    # SINGLE CHOICE SUCCESS
    # ==================================

    return render_template(

        "vote/vote_success.html",

        election=election,

        candidate=candidate
    )