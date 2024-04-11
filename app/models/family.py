from app.extensions import db
from uuid import uuid4


class Family(db.Model):
    __tablename__ = 'family'
    id = db.Column(db.String(), primary_key=True, default=str(uuid4()))
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Family "{self.name}">'
