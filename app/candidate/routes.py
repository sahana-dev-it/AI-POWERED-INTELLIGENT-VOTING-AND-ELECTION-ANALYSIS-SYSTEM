# Import Blueprint, render_template, request, redirect and flash
from flask import Blueprint, render_template, request, redirect, flash

# Import database
from app import db

# Import Candidate model
from app.models.candidate import Candidate

# Import Election model
from app.models.election import Election


# Create Blueprint
candidate = Blueprint(
    "candidate",
    __name__,
    url_prefix="/candidate"
)


# ----------------------------------
# Create Candidate
# ----------------------------------
@candidate.route("/create", methods=["GET", "POST"])
def create():

    elections = Election.query.all()

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

        db.session.add(new_candidate)
        db.session.commit()

        flash("Candidate added successfully!", "success")

        return redirect("/candidate/list")

    return render_template(
        "candidate/create.html",
        elections=elections
    )


# ----------------------------------
# View All Candidates
# ----------------------------------
@candidate.route("/list")
def list_candidates():

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

    db.session.delete(candidate)
    db.session.commit()

    flash("Candidate deleted successfully!", "success")

    return redirect("/candidate/list")


# ----------------------------------
# Edit Candidate
# ----------------------------------
@candidate.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_candidate(id):

    candidate = Candidate.query.get_or_404(id)

    elections = Election.query.all()

    if request.method == "POST":

        candidate.election_id = request.form["election_id"]
        candidate.name = request.form["name"]
        candidate.age = request.form["age"]
        candidate.gender = request.form["gender"]
        candidate.party = request.form["party"]
        candidate.education = request.form["education"]
        candidate.profession = request.form["profession"]
        candidate.manifesto = request.form["manifesto"]

        db.session.commit()

        flash("Candidate updated successfully!", "success")

        return redirect("/candidate/list")

    return render_template(
        "candidate/edit.html",
        candidate=candidate,
        elections=elections
    )