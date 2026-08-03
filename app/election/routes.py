# Import Flask tools
from flask import Blueprint, render_template, request, redirect, flash

# Import database
from app import db

# Import Election model
from app.models.election import Election

# Import datetime
from datetime import datetime


# ----------------------------------
# Election Blueprint
# ----------------------------------

election = Blueprint(
    "election",
    __name__,
    url_prefix="/election"
)


# ----------------------------------
# Function to automatically update
# election status
# ----------------------------------

def update_election_status(election_item):

    # Get current date and time
    now = datetime.now()

    # Convert start date + time into datetime
    start_datetime = datetime.strptime(
        f"{election_item.start_date} "
        f"{election_item.start_time}",
        "%Y-%m-%d %H:%M"
    )

    # Convert end date + time into datetime
    end_datetime = datetime.strptime(
        f"{election_item.end_date} "
        f"{election_item.end_time}",
        "%Y-%m-%d %H:%M"
    )

    # Before election starts
    if now < start_datetime:

        election_item.status = "Upcoming"

    # Election is currently running
    elif start_datetime <= now <= end_datetime:

        election_item.status = "Active"

    # Election has ended
    else:

        election_item.status = "Completed"


# ----------------------------------
# Create Election
# ----------------------------------

@election.route(
    "/create",
    methods=["GET", "POST"]
)
def create():

    if request.method == "POST":

        # Get form data
        title = request.form["title"]
        description = request.form["description"]

        start_date = request.form["start_date"]
        start_time = request.form["start_time"]

        end_date = request.form["end_date"]
        end_time = request.form["end_time"]


        # ----------------------------------
        # Validate date and time
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

        except ValueError:

            flash(
                "Invalid date or time format.",
                "danger"
            )

            return render_template(
                "election/create.html"
            )


        # End time must be after start time
        if end_datetime <= start_datetime:

            flash(
                "Election end time must be after start time.",
                "danger"
            )

            return render_template(
                "election/create.html"
            )


        # ----------------------------------
        # Determine initial status
        # ----------------------------------

        now = datetime.now()

        if now < start_datetime:

            status = "Upcoming"

        elif start_datetime <= now <= end_datetime:

            status = "Active"

        else:

            status = "Completed"


        # ----------------------------------
        # Create Election
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


        # Save election
        db.session.add(new_election)

        db.session.commit()


        flash(
            "Election created successfully!",
            "success"
        )


        return redirect(
            "/election/list"
        )


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


    # Update status for every election
    for election_item in elections:

        update_election_status(
            election_item
        )


    # Save updated statuses
    db.session.commit()


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

    election_item = Election.query.get_or_404(id)


    if request.method == "POST":

        # Update election information
        election_item.title = request.form[
            "title"
        ]

        election_item.description = request.form[
            "description"
        ]

        election_item.start_date = request.form[
            "start_date"
        ]

        election_item.start_time = request.form[
            "start_time"
        ]

        election_item.end_date = request.form[
            "end_date"
        ]

        election_item.end_time = request.form[
            "end_time"
        ]


        # ----------------------------------
        # Validate date and time
        # ----------------------------------

        try:

            start_datetime = datetime.strptime(
                f"{election_item.start_date} "
                f"{election_item.start_time}",
                "%Y-%m-%d %H:%M"
            )

            end_datetime = datetime.strptime(
                f"{election_item.end_date} "
                f"{election_item.end_time}",
                "%Y-%m-%d %H:%M"
            )

        except ValueError:

            flash(
                "Invalid date or time format.",
                "danger"
            )

            return render_template(
                "election/edit.html",
                election=election_item
            )


        # End time must be after start time
        if end_datetime <= start_datetime:

            flash(
                "Election end time must be after start time.",
                "danger"
            )

            return render_template(
                "election/edit.html",
                election=election_item
            )


        # Automatically determine status
        update_election_status(
            election_item
        )


        # Save changes
        db.session.commit()


        flash(
            "Election updated successfully!",
            "success"
        )


        return redirect(
            "/election/list"
        )


    return render_template(
        "election/edit.html",
        election=election_item
    )


# ----------------------------------
# Delete Election
# ----------------------------------

@election.route(
    "/delete/<int:id>"
)
def delete_election(id):

    election_item = Election.query.get_or_404(id)


    db.session.delete(
        election_item
    )

    db.session.commit()


    flash(
        "Election deleted successfully!",
        "success"
    )


    return redirect(
        "/election/list"
    )