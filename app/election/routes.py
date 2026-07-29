# Import Blueprint, render_template and request
from flask import Blueprint, render_template, request, redirect

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


# Create Election Page
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

    return render_template("election/create.html")
# View All Elections
@election.route("/list")
def list_elections():

    # Get all elections from the database
    elections = Election.query.all()

    # Display them in the HTML page
    return render_template(
        "election/list.html",
        elections=elections
    )
# Delete Election
@election.route("/delete/<int:id>")
def delete_election(id):

    # Find the election by ID
    election = Election.query.get_or_404(id)

    # Delete it from the database
    db.session.delete(election)

    # Save changes
    db.session.commit()

    # Return to the election list
    return redirect("/election/list")