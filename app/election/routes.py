# Import Blueprint, render_template, request, redirect and flash
from flask import Blueprint, render_template, request, redirect, flash

# Import database
from app import db

# Import Election model
from app.models.election import Election


# Create Blueprint
election = Blueprint(
    "election",
    __name__,
    url_prefix="/election"
)


# ----------------------------
# Create Election
# ----------------------------
@election.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        start_date = request.form["start_date"]
        start_time = request.form["start_time"]

        end_date = request.form["end_date"]
        end_time = request.form["end_time"]

        status = request.form["status"]

        new_election = Election(
            title=title,
            description=description,
            start_date=start_date,
            start_time=start_time,
            end_date=end_date,
            end_time=end_time,
            status=status
        )

        db.session.add(new_election)
        db.session.commit()

        flash("Election created successfully!", "success")

        return redirect("/election/list")

    return render_template("election/create.html")


# ----------------------------
# View All Elections
# ----------------------------
@election.route("/list")
def list_elections():

    elections = Election.query.all()

    return render_template(
        "election/list.html",
        elections=elections
    )


# ----------------------------
# Edit Election
# ----------------------------
@election.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_election(id):

    election = Election.query.get_or_404(id)

    if request.method == "POST":

        election.title = request.form["title"]
        election.description = request.form["description"]

        election.start_date = request.form["start_date"]
        election.start_time = request.form["start_time"]

        election.end_date = request.form["end_date"]
        election.end_time = request.form["end_time"]

        election.status = request.form["status"]

        db.session.commit()

        flash("Election updated successfully!", "success")

        return redirect("/election/list")

    return render_template(
        "election/edit.html",
        election=election
    )


# ----------------------------
# Delete Election
# ----------------------------
@election.route("/delete/<int:id>")
def delete_election(id):

    election = Election.query.get_or_404(id)

    db.session.delete(election)

    db.session.commit()

    flash("Election deleted successfully!", "success")

    return redirect("/election/list")