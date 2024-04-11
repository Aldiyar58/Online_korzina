from app.extensions import db
from app.models import User


class Profile(db.Model):
    __tablename__ = 'profile'
    user_id = db.Column(db.String(), db.ForeignKey('user.id'), primary_key=True)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Profile "{self.id}">'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
