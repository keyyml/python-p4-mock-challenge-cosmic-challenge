#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/scientists', methods = ['GET', 'POST'])
def scientists():
    if request.method == 'GET':
        scientists = Scientist.query.all()
        scientists_dict = [scientist.to_dict() for scientist in scientists]

        return make_response(scientists_dict, 200)
    
    elif request.method == 'POST':
        form_data = request.get_json()

        try:

            new_scientist = Scientist(
                name = form_data['name'],
                field_of_study = form_data['field_of_study']
            )

            db.session.add(new_scientist)

            db.session.commit()
            
            new_scientist_dict = new_scientist.to_dict()

            return make_response(new_scientist_dict, 201)
        
        except KeyError:

            return make_response({ "validation errors" : None }, 400)

    
@app.route('/scientists/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def scientist_by_id(id):
    
    scientist = Scientist.query.filter_by(id = id).first()

    if scientist:
        if request.method == 'GET':
            scientist_dict = scientist.to_dict()
            return make_response(scientist_dict, 200)
        
        elif request.method == 'PATCH':
            form_data = request.get_json()

            try:
                for attr in form_data:
                    setattr(scientist, attr, form_data.get(attr))
                
                db.session.commit()

                return make_response(scientist.to_dict(), 201)
            
            except KeyError:

                return make_response({ "validation errors" : None }, 403)
            
        elif request.method == 'DELETE':

            db.session.delete(scientist)

            db.session.commit()

            return make_response({}, 202)

    else: 
        return make_response("Scientist not found", 404)

    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
