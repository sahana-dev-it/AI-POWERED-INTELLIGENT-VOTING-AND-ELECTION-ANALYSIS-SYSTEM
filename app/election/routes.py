# ==========================================
# app/election/routes.py
# ==========================================

# ------------------------------------------
# Import Flask tools
# ------------------------------------------

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    session
)


# ------------------------------------------
# Import database
# ------------------------------------------

from app import db


# ------------------------------------------
# Import Election model
# ------------------------------------------

from app.models.election import Election


# ------------------------------------------
# Import datetime
# ------------------------------------------

from datetime import datetime


# ==========================================
# CREATE ELECTION BLUEPRINT
# ==========================================

election = Blueprint(
    "election",
    __name__,
    url_prefix="/election"
)


# ==========================================
# FUNCTION: UPDATE ELECTION STATUS
# ==========================================

def update_election_status(election_item):

    # --------------------------------------
    # Get current date and time
    # --------------------------------------

    now = datetime.now()


    # --------------------------------------
    # Convert start date + time to datetime
    # --------------------------------------

    start_datetime = datetime.strptime(
        f"{election_item.start_date} "
        f"{election_item.start_time}",
        "%Y-%m-%d %H:%M"
    )


    # --------------------------------------
    # Convert end date + time to datetime
    # --------------------------------------

    end_datetime = datetime.strptime(
        f"{election_item.end_date} "
        f"{election_item.end_time}",
        "%Y-%m-%d %H:%M"
    )


    # --------------------------------------
    # Election has not started
    # --------------------------------------

    if now < start_datetime:

        election_item.status = "Upcoming"


    # --------------------------------------
    # Election is currently running
    # --------------------------------------

    elif start_datetime <= now <= end_datetime:

        election_item.status = "Active"


    # --------------------------------------
    # Election has ended
    # --------------------------------------

    else:

        election_item.status = "Completed"


# ==========================================
# CREATE ELECTION
# ==========================================

@election.route(
    "/create",
    methods=["GET", "POST"]
)
def create():

    # --------------------------------------
    # If form is submitted
    # --------------------------------------

    if request.method == "POST":

        # ----------------------------------
        # Get form data
        # ----------------------------------

        title = request.form.get(
            "title",
            ""
        ).strip()


        description = request.form.get(
            "description",
            ""
        ).strip()


        start_date = request.form.get(
            "start_date",
            ""
        ).strip()


        start_time = request.form.get(
            "start_time",
            ""
        ).strip()


        end_date = request.form.get(
            "end_date",
            ""
        ).strip()


        end_time = request.form.get(
            "end_time",
            ""
        ).strip()


        # ----------------------------------
        # Get election type
        # ----------------------------------

        election_type = request.form.get(
            "election_type",
            "single"
        ).strip()


        # ----------------------------------
        # Make sure election type is valid
        # ----------------------------------

        if election_type not in [
            "single",
            "multiple"
        ]:

            election_type = "single"


        # ----------------------------------
        # Check required fields
        # ----------------------------------

        if not title or not description:

            flash(
                "Please fill in all required election information.",
                "danger"
            )

            return render_template(
                "election/create.html"
            )


        # ----------------------------------
        # Convert dates and times
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


        # ----------------------------------
        # End must be after start
        # ----------------------------------

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


        # ==================================
        # CREATE NEW ELECTION
        # ==================================

        new_election = Election(

            title=title,

            description=description,

            start_date=start_date,

            start_time=start_time,

            end_date=end_date,

            end_time=end_time,

            election_type=election_type,

            status=status
        )


        # ==================================
        # SAVE NEW ELECTION
        # ==================================

        db.session.add(
            new_election
        )

        db.session.commit()


        # ==================================
        # IMPORTANT
        # Remember the newly created
        # election AFTER it has been saved.
        # ==================================

        session["selected_election"] = new_election.id


        # ----------------------------------
        # Success message
        # ----------------------------------

        flash(
            "Election created successfully! Now add candidates.",
            "success"
        )


        # ==================================
        # GO TO ADD CANDIDATE PAGE
        # ==================================

        return redirect(
            "/candidate/create"
        )


    # ==================================
    # DISPLAY CREATE ELECTION PAGE
    # ==================================

    return render_template(
        "election/create.html"
    )


# ==========================================
# VIEW ALL ELECTIONS
# ==========================================

@election.route("/list")
def list_elections():

    # --------------------------------------
    # Get all elections
    # --------------------------------------

    elections = Election.query.all()


    # --------------------------------------
    # Automatically update their status
    # --------------------------------------

    for election_item in elections:

        update_election_status(
            election_item
        )


    # --------------------------------------
    # Save updated statuses
    # --------------------------------------

    db.session.commit()


    # --------------------------------------
    # Display election list
    # --------------------------------------

    return render_template(
        "election/list.html",
        elections=elections
    )


# ==========================================
# EDIT ELECTION
# ==========================================

@election.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_election(id):

    # --------------------------------------
    # Find election
    # --------------------------------------

    election_item = Election.query.get_or_404(
        id
    )


    # ======================================
    # UPDATE ELECTION
    # ======================================

    if request.method == "POST":

        # ----------------------------------
        # Get form data
        # ----------------------------------

        election_item.title = request.form.get(
            "title",
            ""
        ).strip()


        election_item.description = request.form.get(
            "description",
            ""
        ).strip()


        election_item.start_date = request.form.get(
            "start_date",
            ""
        ).strip()


        election_item.start_time = request.form.get(
            "start_time",
            ""
        ).strip()


        election_item.end_date = request.form.get(
            "end_date",
            ""
        ).strip()


        election_item.end_time = request.form.get(
            "end_time",
            ""
        ).strip()


        # ----------------------------------
        # Get election type
        # ----------------------------------

        election_type = request.form.get(
            "election_type",
            "single"
        ).strip()


        # ----------------------------------
        # Validate election type
        # ----------------------------------

        if election_type not in [
            "single",
            "multiple"
        ]:

            election_type = "single"


        election_item.election_type = election_type


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


        # ----------------------------------
        # Check end time
        # ----------------------------------

        if end_datetime <= start_datetime:

            flash(
                "Election end time must be after start time.",
                "danger"
            )

            return render_template(
                "election/edit.html",
                election=election_item
            )


        # ----------------------------------
        # Automatically update status
        # ----------------------------------

        update_election_status(
            election_item
        )


        # ----------------------------------
        # Save changes
        # ----------------------------------

        db.session.commit()


        # ----------------------------------
        # Success message
        # ----------------------------------

        flash(
            "Election updated successfully!",
            "success"
        )


        # ----------------------------------
        # Return to election list
        # ----------------------------------

        return redirect(
            "/election/list"
        )


    # ======================================
    # DISPLAY EDIT PAGE
    # ======================================

    return render_template(
        "election/edit.html",
        election=election_item
    )


# ==========================================
# DELETE ELECTION
# ==========================================

@election.route(
    "/delete/<int:id>"
)
def delete_election(id):

    # --------------------------------------
    # Find election
    # --------------------------------------

    election_item = Election.query.get_or_404(
        id
    )


    # --------------------------------------
    # Delete election
    # --------------------------------------

    db.session.delete(
        election_item
    )


    # --------------------------------------
    # Save changes
    # --------------------------------------

    db.session.commit()


    # --------------------------------------
    # Success message
    # --------------------------------------

    flash(
        "Election deleted successfully!",
        "success"
    )


    # --------------------------------------
    # Return to election list
    # --------------------------------------

    return redirect(
        "/election/list"
    )