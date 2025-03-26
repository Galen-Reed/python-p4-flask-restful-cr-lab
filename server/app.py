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
    pass

class PlantByID(Resource):
    pass

@app.route('/plants')
def index_plants():
    plants = [plant.to_dict() for plant in Plant.query.all()]

    return make_response(plants, 200)

@app.route('/plants/<int:id>')
def show_plants(id):
    plant = db.session.get(Plant, id)

    plant_dict = plant.to_dict()

    return make_response(plant_dict, 200)

@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()

    new_plant = Plant(
        name = data['name'],
        image = data['image'],
        price = data['price']
        )

    db.session.add(new_plant)
    db.session.commit()

    return make_response(new_plant.to_dict(), 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
