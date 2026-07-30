from app import db


class Vote(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    voter_id = db.Column(db.Integer, nullable=False)

    election_id = db.Column(db.Integer, nullable=False)

    candidate_id = db.Column(db.Integer, nullable=False)

    vote_time = db.Column(db.String(30), nullable=False)