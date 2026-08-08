from app import db


class Candidate(db.Model):

    # ----------------------------------
    # Candidate ID
    # ----------------------------------

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # ----------------------------------
    # Election ID
    # ----------------------------------

    election_id = db.Column(
        db.Integer,
        db.ForeignKey("election.id"),
        nullable=False
    )


    # ----------------------------------
    # Candidate Name
    # ----------------------------------

    name = db.Column(
        db.String(150),
        nullable=False
    )


    # ----------------------------------
    # Candidate Age
    # ----------------------------------

    age = db.Column(
        db.Integer,
        nullable=False
    )


    # ----------------------------------
    # Gender
    # ----------------------------------

    gender = db.Column(
        db.String(20),
        nullable=False
    )


    # ----------------------------------
    # Party Name
    # ----------------------------------

    party = db.Column(
        db.String(150),
        nullable=False
    )


    # ----------------------------------
    # Education
    # ----------------------------------

    education = db.Column(
        db.String(150),
        nullable=False
    )


    # ----------------------------------
    # Profession
    # ----------------------------------

    profession = db.Column(
        db.String(150),
        nullable=False
    )


    # ----------------------------------
    # Manifesto
    # ----------------------------------

    manifesto = db.Column(
        db.Text,
        nullable=False
    )


    # ----------------------------------
    # Position
    # ----------------------------------

    position = db.Column(
        db.String(100),
        nullable=True
    )