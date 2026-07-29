# Import database object
from app import db


# Election Table
class Election(db.Model):

    # Table name
    __tablename__ = "election"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Election Title
    title = db.Column(db.String(150), nullable=False)

    # Election Description
    description = db.Column(db.Text, nullable=False)

    # Start Date
    start_date = db.Column(db.String(30), nullable=False)

    # End Date
    end_date = db.Column(db.String(30), nullable=False)

    # Election Status
    status = db.Column(db.String(20), default="Upcoming")