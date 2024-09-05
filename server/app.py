#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        response_dict = [n.to_dict() for n in Plant.query.all()]
        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response

class Plants(Resource):
    def post(self):
        try:
            new_plant = Plant(
                name=request.json.get('name'),
                image=request.json.get('image'),
                price=request.json.get('price')
            )

            db.session.add(new_plant)
            db.session.commit()

            response_dict = new_plant.to_dict()
            response = make_response(jsonify(response_dict), 201)
            return response
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 400)

        

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()  # Retrieve the plant by ID
        if plant is None:  # Check if plant exists
            return make_response(jsonify({"error": "Plant not found"}), 404)

        response_dict = plant.to_dict()
        response = make_response(jsonify(response_dict), 200)
        return response
    
    def post(self):
        new_plant = Plant(
            name=request.form['name'],
            image=request.form['image'],
            price=request.form['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        response_dict = new_plant.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response

api.add_resource(Plants, '/plants')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
