# Import Blueprint, render_template, request, redirect and flash
from flask import Blueprint, render_template, request, redirect, flash

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

    # ----------------------------------
    # Add Candidate
    # ----------------------------------

    if request.method == "POST":

        new_candidate = Candidate(

            election_id=request.form["election_id"],

            name=request.form["name"],

            age=request.form["age"],

            gender=request.form["gender"],

            party=request.form["party"],

            education=request.form["education"],

            profession=request.form["profession"],

            manifesto=request.form["manifesto"]

        )

        # Add candidate to database
        db.session.add(new_candidate)

        # Save candidate
        db.session.commit()

        # Success message
        flash(
            "Candidate added successfully! You can add another candidate.",
            "success"
        )

        # ----------------------------------
        # IMPORTANT
        # Stay on Add Candidate page
        # ----------------------------------

        return redirect(
            "/candidate/create"
        )

    # Display Add Candidate page
    return render_template(
        "candidate/create.html",
        elections=elections
    )


# ----------------------------------
# View All Candidates
# ----------------------------------

@candidate.route("/list")
def list_candidates():

    # Get all candidates
    candidates = Candidate.query.all()

    return render_template(
        "candidate/list.html",
        candidates=candidates
    )


# ----------------------------------
# Delete Candidate
# ----------------------------------

@candidate.route("/delete/<int:id>")
def delete_candidate(id):

    candidate = Candidate.query.get_or_404(id)

    # Delete candidate
    db.session.delete(candidate)

    # Save changes
    db.session.commit()

    # Success message
    flash(
        "Candidate deleted successfully!",
        "success"
    )

    return redirect(
        "/candidate/list"
    )


# ----------------------------------
# Edit Candidate
# ----------------------------------

@candidate.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_candidate(id):

    candidate = Candidate.query.get_or_404(id)

    # Get elections for dropdown
    elections = Election.query.all()

    # ----------------------------------
    # Update Candidate
    # ----------------------------------

    if request.method == "POST":

        candidate.election_id = request.form[
            "election_id"
        ]

        candidate.name = request.form[
            "name"
        ]

        candidate.age = request.form[
            "age"
        ]

        candidate.gender = request.form[
            "gender"
        ]

        candidate.party = request.form[
            "party"
        ]

        candidate.education = request.form[
            "education"
        ]

        candidate.profession = request.form[
            "profession"
        ]

        candidate.manifesto = request.form[
            "manifesto"
        ]

        # Save changes
        db.session.commit()

        # Success message
        flash(
            "Candidate updated successfully!",
            "success"
        )

        return redirect(
            "/candidate/list"
        )

    # Display edit page
    return render_template(
        "candidate/edit.html",

        candidate=candidate,

        elections=elections
    )