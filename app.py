import os
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake
from forms import AddCupcakeForm
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.app_context().push()

if os.environ['FLASK_ENV'] == "testing":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
    app.config['WTF_CSRF_ENABLED'] = False
else: 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

##################################################################################################################################
@app.route("/")
def home_page():
    """ Renders base template of html that includes all cupcakes with information about them.
    There is a form that allows for a new cupcake to be added """
    
    form = AddCupcakeForm()

    return render_template('base.html', form=form)


@app.route("/api/cupcakes")
def all_cupcakes():
    """ Returns json data of all cupcakes from database within api

    json return format: {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """ Returns json data of individual cupcake from database within api

    json return format: {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """ Returns json data of newly created cupcake from database within api and status code of 201. 
    If there is an error, returns status code of 400 with error message. 

    json return format: {cupcake: {id, flavor, size, rating, image}}
    or {errors: {message}}
    """

    form = AddCupcakeForm()
    
    image_url = request.json.get("image", None)
    
    if form.validate_on_submit():
    
        new_cupcake = Cupcake(
            flavor=request.json["flavor"], 
            size=request.json["size"], 
            rating=request.json["rating"],
            image=image_url
        )

        db.session.add(new_cupcake)
        db.session.commit()
        response_json = jsonify(cupcake=new_cupcake.serialize())
        return (response_json, 201)
    
    else: 
        error_messages = form.errors
        return jsonify(errors=error_messages), 400

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """ Returns json data of updated cupcake from database within api

    json return format: {cupcake: {id, flavor, size, rating, image}}"""

    # add conditional logic to handle errors with different keys submitted 
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.query(Cupcake).filter_by(id=cupcake_id).update(request.json)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Returns json data of newly created cupcake from database within api

    json return format: {message: "Deleted"}"""
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
