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
    
    return app

if __name__ == '__main__':
    app = create_app('cupcakes')
    connect_db(app)
    app.run(debug=True)