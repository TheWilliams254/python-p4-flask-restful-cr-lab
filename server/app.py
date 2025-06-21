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
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])
    
    def post(self):
        new_plant = Plant(
            name=request.json['name'],
            image=request.json['image'],
            price=request.json['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(jsonify(new_plant.to_dict()), 201)
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        return jsonify(plant.to_dict())
    
api.add_resource(PlantByID, '/plants/<int:id>')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
