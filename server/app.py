from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>API for tracking heroes and their superpowers</h1>'

@app.route('/heroes')
def heroes():
    heroes = [hero.to_dict(rules=('-hero_powers', )) for hero in Hero.query.all()]
    return make_response(jsonify(heroes), 200)

@app.route('/heroes/<int:id>')
def hero_by_id(id):
    hero = Hero.query.filter_by(id = id).first()
    if hero:
        hero_serialized = hero.to_dict()
        return make_response(jsonify(hero_serialized), 200)
    else:
        response_body = {
            "error": "Hero not found"
        }
        return make_response(jsonify(response_body), 400)

@app.route('/powers')
def powers():
    powers = [power.to_dict(rules=('-hero_powers', )) for power in Power.query.all()]
    return make_response(jsonify(powers), 200)

@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def power_by_id(id):
    power = Power.query.filter_by(id = id).first()
    if request.method == 'GET':
        if power:
            power_serialized = power.to_dict(rules=('-hero_powers', ))
            return make_response(jsonify(power_serialized), 200)
        else:
            response_body = {
                "error": "Power not found"
            }
            return make_response(jsonify(response_body), 404)
    elif request.method == 'PATCH':
        if not power:
            response_body = {
                "error": "Power not found"
            }
            return make_response(jsonify(response_body), 404)
        data = request.json
        new_description = data.get('description', None)

        if not new_description or len(new_description) < 20:
            response_body = {
                "errors": ["validation errors"]
            }
            return make_response(jsonify(response_body), 400)
        power.description = new_description
        db.session.commit()
        power_dict = power.to_dict(rules=('-hero_powers', ))
        return make_response(power_dict, 200)

@app.route('/hero_powers', methods=['POST'])
def hero_powers():
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
