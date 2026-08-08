# Import Blueprint, render_template, request, redirect, flash and session
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


# ----------------------------------
# Create Candidate
# ----------------------------------

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

        # Remember selected election
        session["selected_election"] = request.form[
            "election_id"
        ]

        # Get selected election
        selected_election_id = int(
            request.form["election_id"]
        )

        selected_election_object = Election.query.get_or_404(
            selected_election_id
        )

        # ----------------------------------
        # Get Position
        # ----------------------------------

        position = request.form.get(
            "position",
            ""
        ).strip()

        # ----------------------------------
        # Position is required only for
        # Multiple Positions elections
        # ----------------------------------

        if (
            selected_election_object.election_type == "multiple"
            and not position
        ):

            flash(
                "Please enter the candidate position.",
                "danger"
            )

            return redirect(
                "/candidate/create"
            )

        # ----------------------------------
        # For Single Choice elections,
        # position is not required
        # ----------------------------------

        if selected_election_object.election_type == "single":

            position = None

        # ----------------------------------
        # Create Candidate
        # ----------------------------------

        new_candidate = Candidate(

            election_id=selected_election_id,

            name=request.form["name"].strip(),

            age=request.form["age"],

            gender=request.form["gender"],

            party=request.form["party"].strip(),

            education=request.form["education"].strip(),

            profession=request.form["profession"].strip(),

            manifesto=request.form["manifesto"].strip(),

            position=position

        )

        # Add candidate
        db.session.add(new_candidate)

        # Save candidate
        db.session.commit()

        # Success message
        flash(
            "Candidate added successfully! You can add another candidate.",
            "success"
        )

        # Stay on same page
        return redirect(
            "/candidate/create"
        )

    # ----------------------------------
    # Display Add Candidate page
    # ----------------------------------

    return render_template(
        "candidate/create.html",
        elections=elections,
        selected_election=selected_election
    )


# ----------------------------------
# View Candidates
# ----------------------------------

@candidate.route("/list")
def list_candidates():

    # Get all elections
    elections = Election.query.all()

    # Selected election
    selected_election = request.args.get(
        "election_id",
        type=int
    )

    # Default values
    candidates = []

    election = None

    # ----------------------------------
    # If an election is selected
    # ----------------------------------

    if selected_election:

        election = Election.query.get_or_404(
            selected_election
        )

        candidates = Candidate.query.filter_by(
            election_id=selected_election
        ).order_by(
            Candidate.id
        ).all()

    # ----------------------------------
    # Display candidates
    # ----------------------------------

    return render_template(

        "candidate/list.html",

        elections=elections,

        candidates=candidates,

        selected_election=selected_election,

        election=election

    )


# ----------------------------------
# Delete Candidate
# ----------------------------------

@candidate.route(
    "/delete/<int:id>"
)
def delete_candidate(id):

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


# ----------------------------------
# Edit Candidate
# ----------------------------------

@candidate.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_candidate(id):

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
        new_election_id = int(
            request.form["election_id"]
        )

        new_election = Election.query.get_or_404(
            new_election_id
        )

        # Get position
        position = request.form.get(
            "position",
            ""
        ).strip()

        # ----------------------------------
        # Position required for
        # Multiple Positions elections
        # ----------------------------------

        if (
            new_election.election_type == "multiple"
            and not position
        ):

            flash(
                "Please enter the candidate position.",
                "danger"
            )

            return render_template(
                "candidate/edit.html",
                candidate=candidate_item,
                elections=elections
            )

        # ----------------------------------
        # Single Choice election
        # ----------------------------------

        if new_election.election_type == "single":

            position = None

        # ----------------------------------
        # Update candidate information
        # ----------------------------------

        candidate_item.election_id = new_election_id

        candidate_item.name = request.form[
            "name"
        ].strip()

        candidate_item.age = request.form[
            "age"
        ]

        candidate_item.gender = request.form[
            "gender"
        ]

        candidate_item.party = request.form[
            "party"
        ].strip()

        candidate_item.education = request.form[
            "education"
        ].strip()

        candidate_item.profession = request.form[
            "profession"
        ].strip()

        candidate_item.manifesto = request.form[
            "manifesto"
        ].strip()

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
            f"/candidate/list?election_id={new_election_id}"
        )

    # ----------------------------------
    # Display Edit Candidate page
    # ----------------------------------

    return render_template(
        "candidate/edit.html",

        candidate=candidate_item,

        elections=elections
    )