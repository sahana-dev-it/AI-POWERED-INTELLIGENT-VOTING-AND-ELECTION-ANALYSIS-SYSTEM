# Import Flask tools

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    session
)


# Import database

from app import db


# Import Candidate model

from app.models.candidate import Candidate


# Import Election model

from app.models.election import Election


# ----------------------------------
# Create Candidate Blueprint
# ----------------------------------

candidate = Blueprint(
    "candidate",
    __name__,
    url_prefix="/candidate"
)


# ==================================
# CREATE CANDIDATE
# ==================================

@candidate.route(
    "/create",
    methods=["GET", "POST"]
)
def create():

    # Get all elections

    elections = Election.query.all()


    # Previously selected election

    selected_election = session.get(
        "selected_election"
    )


    # ----------------------------------
    # Add Candidate
    # ----------------------------------

    if request.method == "POST":

        # Get selected election ID

        election_id = request.form.get(
            "election_id",
            type=int
        )


        # Make sure election exists

        election = Election.query.get_or_404(
            election_id
        )


        # Remember selected election

        session["selected_election"] = election_id


        # ----------------------------------
        # Get Position
        # ----------------------------------

        position = request.form.get(
            "position",
            ""
        ).strip()


        # ----------------------------------
        # Position rules
        # ----------------------------------

        # Multiple-position election
        # must have a position

        if election.election_type == "multiple":

            if not position:

                flash(
                    "Please enter the candidate position.",
                    "danger"
                )

                return render_template(
                    "candidate/create.html",
                    elections=elections,
                    selected_election=selected_election
                )


        # Single-position election
        # does not need position

        else:

            position = None


        # ----------------------------------
        # Create Candidate
        # ----------------------------------

        new_candidate = Candidate(

            election_id=election_id,

            name=request.form["name"],

            age=request.form["age"],

            gender=request.form["gender"],

            party=request.form["party"],

            education=request.form["education"],

            profession=request.form["profession"],

            manifesto=request.form["manifesto"],

            position=position

        )


        # Add candidate

        db.session.add(
            new_candidate
        )


        # Save candidate

        db.session.commit()


        # ----------------------------------
        # Success Message
        # ----------------------------------

        flash(
            "Candidate added successfully! You can add another candidate.",
            "success"
        )


        # Stay on same page

        return redirect(
            "/candidate/create"
        )


    # ----------------------------------
    # Display Create Page
    # ----------------------------------

    return render_template(
        "candidate/create.html",
        elections=elections,
        selected_election=selected_election
    )


# ==================================
# VIEW CANDIDATES
# ==================================

@candidate.route("/list")
def list_candidates():

    # Get all elections

    elections = Election.query.all()


    # Get selected election

    selected_election = request.args.get(
        "election_id",
        type=int
    )


    # Default values

    candidates = []

    election = None


    # ----------------------------------
    # If election selected
    # ----------------------------------

    if selected_election:

        election = Election.query.get_or_404(
            selected_election
        )


        # Get candidates for this election

        candidates = Candidate.query.filter_by(
            election_id=selected_election
        ).order_by(
            Candidate.id
        ).all()


    # ----------------------------------
    # Display Candidate List
    # ----------------------------------

    return render_template(
        "candidate/list.html",

        elections=elections,

        candidates=candidates,

        selected_election=selected_election,

        election=election
    )


# ==================================
# DELETE CANDIDATE
# ==================================

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


    # Save changes

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


# ==================================
# EDIT CANDIDATE
# ==================================

@candidate.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_candidate(id):

    # Find candidate

    candidate_item = Candidate.query.get_or_404(
        id
    )


    # Get all elections

    elections = Election.query.all()


    # ----------------------------------
    # Update Candidate
    # ----------------------------------

    if request.method == "POST":

        # Get selected election

        election_id = request.form.get(
            "election_id",
            type=int
        )


        # Make sure election exists

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


        # ----------------------------------
        # Update candidate information
        # ----------------------------------

        candidate_item.election_id = election_id


        candidate_item.name = request.form[
            "name"
        ]


        candidate_item.age = request.form[
            "age"
        ]


        candidate_item.gender = request.form[
            "gender"
        ]


        candidate_item.party = request.form[
            "party"
        ]


        candidate_item.education = request.form[
            "education"
        ]


        candidate_item.profession = request.form[
            "profession"
        ]


        candidate_item.manifesto = request.form[
            "manifesto"
        ]


        # Save position

        candidate_item.position = position


        # Save changes

        db.session.commit()


        # ----------------------------------
        # Success message
        # ----------------------------------

        flash(
            "Candidate updated successfully!",
            "success"
        )


        # Return to selected election

        return redirect(
            f"/candidate/list?election_id={candidate_item.election_id}"
        )


    # ----------------------------------
    # Display Edit Page
    # ----------------------------------

    return render_template(
        "candidate/edit.html",

        candidate=candidate_item,

        elections=elections
    )