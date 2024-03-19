# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter_by(id = id).first()
    if pet:
        body = pet.to_dict()
        status = 200
    else:
        body =  {'message': f'Pet {id} not found.'}
        status = 404
    return make_response(body, status)

@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = Pet.query.filter_by(species = species)
    if pets:
        all_pets = []
        for pet in pets:
            all_pets.append(pet.to_dict())
        body = {'count':len(all_pets),
                'pets': all_pets
                }
        status = 200
    else:
        body =  {'message': f'Pet {species} not found.'}
        status = 404
    return make_response(body,status)
    



if __name__ == '__main__':
    app.run(port=5555, debug=True)
