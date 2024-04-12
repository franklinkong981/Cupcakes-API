"""Seed file to insert multiple cupcakes model objects into the cupcakes database to provide some starter sample data."""
from app import create_app
from models import db, connect_db, Cupcake

app = create_app('cupcakes')
connect_db(app)
app.app_context().push()

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
Cupcake.query.delete()

# Create starting cupcake
c1 = Cupcake(
    flavor="cherry",
    size="large",
    rating=5,
)

c2 = Cupcake(
    flavor="chocolate",
    size="small",
    rating=9,
    image_url="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
)

db.session.add_all([c1, c2])
db.session.commit()