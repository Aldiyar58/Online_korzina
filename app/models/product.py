from app.extensions import db
from flask import jsonify


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    photo = db.Column(db.Text(), nullable=False)
    cost = db.Column(db.Integer(), nullable=False)
    market = db.Column(db.String(), nullable=False)

    ps = db.relationship('ProductList', backref='products')

    def __repr__(self):
        return f'<Product_list "{self.id}">'

    @classmethod
    def get_pasha(cls, category):
        return jsonify(cls.query.filter_by(category=category).all())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
