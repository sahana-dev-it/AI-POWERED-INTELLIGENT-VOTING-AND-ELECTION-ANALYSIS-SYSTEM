from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    session
)

from app import db

from app.models.candidate import Candidate
from app.models.election import Election


# ==========================================
# CREATE CANDIDATE BLUEPRINT
# ==========================================

candidate = Blueprint(
    "candidate",
    __name__,
    url_prefix="/candidate"
)


# ==========================================
# CREATE CANDIDATE
# ==========================================

@candidate.route(
    "/create",
    methods=["GET", "POST"]
)
def create():

    # Get all elections
    elections = Election.query.order_by(
        Election.id.desc()
    ).all()

    # Previously selected election
    selected_election = session.get(
        "selected_election"
    )

    # ======================================
    # ADD CANDIDATE
    # ======================================

    if request.method == "POST":

        # Get election ID
        election_id = request.form.get(
            "election_id",
            type=int
        )

        # Make sure election was selected
        if not election_id:

            flash(
                "Please select an election.",
                "danger"
            )

            return render_template(
                "candidate/create.html",
                elections=elections,
                selected_election=selected_election
            )

        # Find election
        election = Election.query.get_or_404(
            election_id
        )

        # Remember selected election
        session["selected_election"] = election_id

        # ----------------------------------
        # Get position
        # ----------------------------------

        position = request.form.get(
            "position",
            ""
        ).strip()

        # ----------------------------------
        # Position rules
        # ----------------------------------

        if election.election_type == "multiple":

            if not position:

                flash(
                    "Please enter the candidate position.",
                    "danger"
                )

                return render_template(
                    "candidate/create.html",
                    elections=elections,
                    selected_election=election_id
                )

        else:

            # Single Choice election
            # does not use position
            position = None

        # ----------------------------------
        # Create candidate
        # ----------------------------------

        new_candidate = Candidate(

            election_id=election_id,

            name=request.form.get(
                "name",
                ""
            ).strip(),

            age=request.form.get(
                "age",
                ""
            ).strip(),

            gender=request.form.get(
                "gender",
                ""
            ).strip(),

            party=request.form.get(
                "party",
                ""
            ).strip(),

            education=request.form.get(
                "education",
                ""
            ).strip(),

            profession=request.form.get(
                "profession",
                ""
            ).strip(),

            manifesto=request.form.get(
                "manifesto",
                ""
            ).strip(),

            position=position
        )

        # Save candidate
        db.session.add(
            new_candidate
        )

        db.session.commit()

        # Success message
        flash(
            "Candidate added successfully! You can add another candidate.",
            "success"
        )

        # Stay on candidate creation page
        return redirect(
            "/candidate/create"
        )

    # ======================================
    # DISPLAY CREATE PAGE
    # ======================================

    return render_template(
        "candidate/create.html",
        elections=elections,
        selected_election=selected_election
    )


# ==========================================
# VIEW CANDIDATES
# ==========================================

@candidate.route(
    "/list"
)
def list_candidates():

    # ======================================
    # GET ALL ELECTIONS
    # ======================================

    elections = Election.query.order_by(
        Election.id.desc()
    ).all()

    # ======================================
    # GET SELECTED ELECTION
    # ======================================

    selected_election = request.args.get(
        "election_id",
        type=int
    )

    # ======================================
    # GET SELECTED POSITION
    # ======================================

    selected_position = request.args.get(
        "position",
        ""
    ).strip()

    # Default values
    election = None
    candidates = []

    # ======================================
    # IF ELECTION IS SELECTED
    # ======================================

    if selected_election:

        # Find ONLY the selected election
        election = Election.query.get_or_404(
            selected_election
        )

        # ----------------------------------
        # IMPORTANT:
        #
        # Only candidates whose
        # election_id matches the selected
        # election are loaded.
        # ----------------------------------

        candidates_query = Candidate.query.filter(
            Candidate.election_id == selected_election
        )

        # ----------------------------------
        # POSITION FILTER
        # ----------------------------------

        if election.election_type == "multiple":

            if selected_position:

                candidates_query = candidates_query.filter(
                    Candidate.position == selected_position
                )

        # Get candidates
        candidates = candidates_query.order_by(
            Candidate.id.asc()
        ).all()

    # ======================================
    # GET AVAILABLE POSITIONS
    # FOR SELECTED ELECTION
    # ======================================

    positions = []

    if election and election.election_type == "multiple":

        positions = db.session.query(
            Candidate.position
        ).filter(
            Candidate.election_id == election.id,
            Candidate.position.isnot(None),
            Candidate.position != ""
        ).distinct().order_by(
            Candidate.position.asc()
        ).all()

        # Convert tuples into simple strings
        positions = [
            position[0]
            for position in positions
        ]

    # ======================================
    # DISPLAY CANDIDATE LIST
    # ======================================

    return render_template(
        "candidate/list.html",

        elections=elections,

        candidates=candidates,

        selected_election=selected_election,

        selected_position=selected_position,

        election=election,

        positions=positions
    )


# ==========================================
# DELETE CANDIDATE
# ==========================================

@candidate.route(
    "/delete/<int:id>"
)
def delete_candidate(id):

    # Find candidate
    candidate_item = Candidate.query.get_or_404(
        id
    )

    # Remember election
    election_id = candidate_item.election_id

    # Delete candidate
    db.session.delete(
        candidate_item
    )

    db.session.commit()

    # Success message
    flash(
        "Candidate deleted successfully!",
        "success"
    )

    # Return to same election
    return redirect(
        f"/candidate/list?election_id={election_id}"
    )


# ==========================================
# EDIT CANDIDATE
# ==========================================

@candidate.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_candidate(id):

    # ======================================
    # FIND CANDIDATE
    # ======================================

    candidate_item = Candidate.query.get_or_404(
        id
    )

    # Get all elections
    elections = Election.query.order_by(
        Election.id.desc()
    ).all()

    # ======================================
    # UPDATE CANDIDATE
    # ======================================

    if request.method == "POST":

        # Get selected election ID
        election_id = request.form.get(
            "election_id",
            type=int
        )

        # Make sure election was selected
        if not election_id:

            flash(
                "Please select an election.",
                "danger"
            )

            return render_template(
                "candidate/edit.html",
                candidate=candidate_item,
                elections=elections
            )

        # Find election
        election = Election.query.get_or_404(
            election_id
        )

        # ----------------------------------
        # Get position
        # ----------------------------------

        position = request.form.get(
            "position",
            ""
        ).strip()

        # ----------------------------------
        # Position rules
        # ----------------------------------

        if election.election_type == "multiple":

            if not position:

                flash(
                    "Please enter the candidate position.",
                    "danger"
                )

                return render_template(
                    "candidate/edit.html",
                    candidate=candidate_item,
                    elections=elections
                )

        else:

            position = None

        # ==================================
        # UPDATE CANDIDATE DATA
        # ==================================

        candidate_item.election_id = election_id

        candidate_item.name = request.form.get(
            "name",
            ""
        ).strip()

        candidate_item.age = request.form.get(
            "age",
            ""
        ).strip()

        candidate_item.gender = request.form.get(
            "gender",
            ""
        ).strip()

        candidate_item.party = request.form.get(
            "party",
            ""
        ).strip()

        candidate_item.education = request.form.get(
            "education",
            ""
        ).strip()

        candidate_item.profession = request.form.get(
            "profession",
            ""
        ).strip()

        candidate_item.manifesto = request.form.get(
            "manifesto",
            ""
        ).strip()

        candidate_item.position = position

        # Save changes
        db.session.commit()

        # Success message
        flash(
            "Candidate updated successfully!",
            "success"
        )

        # Return to selected election
        return redirect(
            f"/candidate/list?election_id={election_id}"
        )

    # ======================================
    # DISPLAY EDIT PAGE
    # ======================================

    return render_template(
        "candidate/edit.html",
        candidate=candidate_item,
        elections=elections
    )