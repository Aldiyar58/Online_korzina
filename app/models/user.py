from app.extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy import not_
from app.models import Family


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(), primary_key=True, default=str(uuid4()))
    family_id = db.Column(db.String(), db.ForeignKey('family.id'))
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.Text)

    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f'<User "{self.id}">'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_all_user_email(cls):
        real_users = cls.query.filter(not_(cls.email.contains('example'))).all()
        return [user.email for user in real_users]

    @classmethod
    def update_email(cls, email, new_email, password):
        user = cls.query.filter_by(email=email).first()
        if user and user.check_password(password):
            user.email = new_email
            try:
                db.session.commit()
                return True
            except (IntegrityError, OperationalError):
                db.session.rollback()
                return False
        return False

    @classmethod
    def update_password(cls, email, password, new_password):
        user = cls.get_user_by_email(email)
        if user and user.check_password(password):
            try:
                user.set_password(new_password)
                db.session.commit()
                return True
            except (IntegrityError, OperationalError):
                db.session.rollback()
        return False

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
