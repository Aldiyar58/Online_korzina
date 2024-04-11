from app.extensions import db
from app.models import User, Product


class ProductList(db.Model):
    __tablename__ = 'product_list'
    family_id = db.Column(db.String(), primary_key=True)
    product_id = db.Column(db.String(), db.ForeignKey('product.id'), primary_key=True)
    added_name = db.Column(db.String(), nullable=False)
    count = db.Column(db.Integer(), default=1)
    comment = db.Column(db.Text())

    def __repr__(self):
        return f'<Product_list "{self.id}">'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
