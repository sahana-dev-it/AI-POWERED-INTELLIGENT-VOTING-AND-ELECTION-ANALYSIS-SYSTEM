from app.models.candidate import Candidate
# Import Blueprint and render_template
from flask import Blueprint, render_template

# Import Election model
from app.models.election import Election


# Create Blueprint
vote = Blueprint(
    "vote",
    __name__,
    url_prefix="/vote"
)


# ----------------------------------
# Show Active Elections
# ----------------------------------
@vote.route("/elections")
def elections():

    # Get all active elections
    elections = Election.query.filter_by(status="Active").all()

    return render_template(
        "vote/elections.html",
        elections=elections
    )
# Import Candidate model
from app.models.candidate import Candidate


# ----------------------------------
# Show Candidates of Selected Election
# ----------------------------------
@vote.route("/candidates/<int:election_id>")
def candidates(election_id):

    election = Election.query.get_or_404(election_id)

    candidates = Candidate.query.filter_by(
        election_id=election_id
    ).all()

    return render_template(
        "vote/candidates.html",
        election=election,
        candidates=candidates
    )