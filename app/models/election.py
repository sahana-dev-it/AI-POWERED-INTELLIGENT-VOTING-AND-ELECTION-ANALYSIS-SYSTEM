from app import db


class Election(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    start_date = db.Column(
        db.String(20),
        nullable=False
    )

    start_time = db.Column(
        db.String(10),
        nullable=False
    )

    end_date = db.Column(
        db.String(20),
        nullable=False
    )

    end_time = db.Column(
        db.String(10),
        nullable=False
    )

    # ----------------------------------
    # Election Type
    # ----------------------------------

    election_type = db.Column(
        db.String(20),
        nullable=False,
        default="single"
    )

    # ----------------------------------
    # Election Status
    # ----------------------------------

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Upcoming"
    )