from app.extensions import db
from uuid import uuid4


class Family(db.Model):
    __tablename__ = 'family'
    id = db.Column(db.String(), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Family "{self.name}">'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
