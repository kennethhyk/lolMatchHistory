from .app import db
from datetime import datetime

class SearchRecord(db.Model):
    """Tasks for the To Do list."""
    id = db.Column(db.Integer, primary_key=True)
    summoner_name = db.Column(db.Unicode(100), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        """On construction, set date of creation."""
        super().__init__(*args, **kwargs)
        self.creation_date = datetime.now()

    def toDict(self):
        return {
            "summoner_name": self.summoner_name,
            "creation_date": self.creation_date
        }
