# Import Flask tools
from flask import Blueprint, render_template, request, redirect, flash

# Import database
from app import db

# Import Election model
from app.models.election import Election

# Import datetime
from datetime import datetime


# Create Blueprint
election = Blueprint(
    "election",
    __name__,
    url_prefix="/election"
)


# ----------------------------------
# Function to calculate election status
# ----------------------------------

def update_election_status(election):

    try:

        # Convert stored date and time into datetime
        start_datetime = datetime.strptime(
            f"{election.start_date} {election.start_time}",
            "%Y-%m-%d %H:%M"
        )

        end_datetime = datetime.strptime(
            f"{election.end_date} {election.end_time}",
            "%Y-%m-%d %H:%M"
        )

        # Get current date and time
        current_datetime = datetime.now()

        # ----------------------------------
        # Before election starts
        # ----------------------------------

        if current_datetime < start_datetime:

            election.status = "Upcoming"

        # ----------------------------------
        # Election is currently running
        # ----------------------------------

        elif (
            current_datetime >= start_datetime
            and
            current_datetime < end_datetime
        ):

            election.status = "Active"

        # ----------------------------------
        # Election has ended
        # ----------------------------------

        else:

            election.status = "Completed"

    except (ValueError, TypeError):

        # If date/time format is incorrect,
        # keep the existing status
        pass


# ----------------------------------
# Create Election
# ----------------------------------

@election.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "POST":

        title = request.form["title"]

        description = request.form["description"]

        start_date = request.form["start_date"]
        start_time = request.form["start_time"]

        end_date = request.form["end_date"]
        end_time = request.form["end_time"]

        # ----------------------------------
        # Automatically determine status
        # ----------------------------------

        try:

            start_datetime = datetime.strptime(
                f"{start_date} {start_time}",
                "%Y-%m-%d %H:%M"
            )

            end_datetime = datetime.strptime(
                f"{end_date} {end_time}",
                "%Y-%m-%d %H:%M"
            )

            current_datetime = datetime.now()

            if current_datetime < start_datetime:

                status = "Upcoming"

            elif (
                current_datetime >= start_datetime
                and
                current_datetime < end_datetime
            ):

                status = "Active"

            else:

                status = "Completed"

        except ValueError:

            status = "Upcoming"

        # ----------------------------------
        # Create election
        # ----------------------------------

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

        flash(
            "Election created successfully!",
            "success"
        )

        return redirect("/election/list")

    return render_template(
        "election/create.html"
    )


# ----------------------------------
# View All Elections
# ----------------------------------

@election.route("/list")
def list_elections():

    # Get all elections
    elections = Election.query.all()

    # Update status of every election
    for election_item in elections:

        update_election_status(election_item)

    # Save updated statuses
    db.session.commit()

    # Display elections
    return render_template(
        "election/list.html",
        elections=elections
    )


# ----------------------------------
# Edit Election
# ----------------------------------

@election.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_election(id):

    election = Election.query.get_or_404(id)

    if request.method == "POST":

        election.title = request.form["title"]

        election.description = request.form["description"]

        election.start_date = request.form["start_date"]

        election.start_time = request.form["start_time"]

        election.end_date = request.form["end_date"]

        election.end_time = request.form["end_time"]

        # ----------------------------------
        # Automatically calculate status
        # ----------------------------------

        try:

            start_datetime = datetime.strptime(
                f"{election.start_date} {election.start_time}",
                "%Y-%m-%d %H:%M"
            )

            end_datetime = datetime.strptime(
                f"{election.end_date} {election.end_time}",
                "%Y-%m-%d %H:%M"
            )

            current_datetime = datetime.now()

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

        except ValueError:

            election.status = "Upcoming"

        # Save changes
        db.session.commit()

        flash(
            "Election updated successfully!",
            "success"
        )

        return redirect("/election/list")

    return render_template(
        "election/edit.html",
        election=election
    )


# ----------------------------------
# Delete Election
# ----------------------------------

@election.route("/delete/<int:id>")
def delete_election(id):

    election = Election.query.get_or_404(id)

    db.session.delete(election)

    db.session.commit()

    flash(
        "Election deleted successfully!",
        "success"
    )

    return redirect("/election/list")