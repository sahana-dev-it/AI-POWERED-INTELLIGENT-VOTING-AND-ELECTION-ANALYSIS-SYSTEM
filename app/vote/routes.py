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


# Create Vote Blueprint
vote = Blueprint(
    "vote",
    __name__,
    url_prefix="/vote"
)


# ----------------------------------
# Show Active Elections
# ----------------------------------
@vote.route("/elections")
@login_required
def elections():

    elections = Election.query.filter_by(status="Active").all()

    return render_template(
        "vote/elections.html",
        elections=elections
    )


# ----------------------------------
# Show Candidates
# ----------------------------------
@vote.route("/candidates/<int:election_id>")
@login_required
def candidates(election_id):

    election = Election.query.get_or_404(election_id)

    candidates = Candidate.query.filter_by(
        election_id=election_id
    ).all()

    # Check whether current voter has already voted
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


# ----------------------------------
# Cast Vote
# ----------------------------------
@vote.route("/cast/<int:election_id>/<int:candidate_id>", methods=["POST"])
@login_required
def cast_vote(election_id, candidate_id):

    # Find election
    election = Election.query.get_or_404(election_id)

    # Find candidate
    candidate = Candidate.query.get_or_404(candidate_id)

    # Make sure candidate belongs to this election
    if candidate.election_id != election.id:

        flash(
            "Invalid candidate for this election.",
            "danger"
        )

        return redirect("/vote/elections")


    # Check whether voter already voted
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


    # Create vote
    new_vote = Vote(

        voter_id=current_user.id,

        election_id=election.id,

        candidate_id=candidate.id,

        vote_time=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )


    # Save vote
    db.session.add(new_vote)

    db.session.commit()


    flash(
        "Your vote has been successfully recorded!",
        "success"
    )


    return redirect(
        f"/vote/candidates/{election.id}"
    )