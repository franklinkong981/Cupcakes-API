"""This file contains the method for creating an application instance and the routes for the Cupcakes API application."""
from flask import Flask, request, render_template, redirect, flash, jsonify, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

def create_app(db_name, testing=False):
    """Create an instance of the app so I can have a production database and a separate testing database."""
    app = Flask(__name__)
    app.testing = testing
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SECRET_KEY"] = "oh-so-secret"
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    debug = DebugToolbarExtension(app)
    if app.testing:
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
    else:
        app.config['SQLALCHEMY_ECHO'] = True 
    
    @app.route('/api/cupcakes')
    def get_all_cupcakes():
        """Returns information about all the cupackes in the form of JSON. Shows information about their id, flavor, size, rating,
        and image url."""

        all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
        return jsonify(cupcakes=all_cupcakes)
    
    @app.route('/api/cupcakes/<int:cupcake_id>')
    def get_cupcake(cupcake_id):
        """Returns information about a specific cupcake whose id in the cupcakes table matches the cupcake_id provided."""

        cupcake = Cupcake.query.get_or_404(cupcake_id)
        return jsonify(cupcake=cupcake.serialize())
    
    @app.route('/api/cupcakes', methods=["POST"])
    def create_cupcake():
        """Creates a new cupcake with a flavor, size, rating, and optional image url. Adds the new cupcake to the database
        and responds with JSON showing information about the new cupcake added."""

        new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"], image_url=request.json.get('image_url', None))
        db.session.add(new_cupcake)
        db.session.commit()

        response_json = jsonify(cupcake=new_cupcake.serialize())
        return (response_json, 201)

    return app

if __name__ == '__main__':
    app = create_app('cupcakes')
    connect_db(app)
    app.run(debug=True)