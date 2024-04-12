"""This file contains the Cupcake model, which is what this JSON API project is about."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

class Cupcake(db.Model):
    """Cupcake model. Each cupcake should have an id, flavor, size, rating, and image url. Only the image url is optional."""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.Text, nullable=True, default="https://tinyurl.com/demo-cupcake")

    def __repr__(self):
        return f"<Cupcake id: {self.id} flavor: {self.flavor} size: {self.size} rating: {self.rating}"