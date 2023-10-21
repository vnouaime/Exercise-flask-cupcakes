import os
from app import app
from models import db, Cupcake

if os.environ['FLASK_ENV'] == "testing":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
else: 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'

db.drop_all()
db.create_all()

c1 = Cupcake(
    flavor="cherry",
    size="large",
    rating=5,
)

c2 = Cupcake(
    flavor="chocolate",
    size="small",
    rating=9,
    image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
)

db.session.add_all([c1, c2])
db.session.commit()