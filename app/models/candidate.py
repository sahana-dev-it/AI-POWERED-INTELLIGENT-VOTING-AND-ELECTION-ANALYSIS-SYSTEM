from app import db


class Candidate(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    election_id = db.Column(
        db.Integer,
        db.ForeignKey("election.id"),
        nullable=False
    )

    name = db.Column(db.String(100), nullable=False)

    age = db.Column(db.Integer, nullable=False)

    gender = db.Column(db.String(20), nullable=False)

    party = db.Column(db.String(100), nullable=False)

    education = db.Column(db.String(100), nullable=False)

    profession = db.Column(db.String(100), nullable=False)

    manifesto = db.Column(db.Text, nullable=False)