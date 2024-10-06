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
    """Endpoint to get all the heroes in json format"""
    heroes = [hero.to_dict(rules=('-hero_powers', )) for hero in Hero.query.all()]
    return make_response(jsonify(heroes), 200)

@app.route('/heroes/<int:id>')
def hero_by_id(id):
    """Endpoint to get hero with specified id."""
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
    """Endpoint to get all the powers in json format"""
    powers = [power.to_dict(rules=('-hero_powers', )) for power in Power.query.all()]
    return make_response(jsonify(powers), 200)

@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def power_by_id(id):
    """Endpoint to get or update power with specified id."""
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
    """Endpoint o post a new hero_power"""
    data = request.json
    strength = data.get('strength')
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')

    hero = Hero.query.filter_by(id = hero_id).first()
    power = Power.query.filter_by(id = power_id).first()
    
    if not hero or not power:
        response_body = {
            "errors": ["Hero or Power not found"]
        }
        return make_response(jsonify(response_body), 404)
        
    valid_strengths = ['Strong', 'Weak', 'Average']
    if strength.title() not in valid_strengths:
        response_body = {
            "errors": ["Validation errors"]
        }
        return make_response(jsonify(response_body), 400)

    new_hero_power = HeroPower(strength = strength, hero_id = hero_id, power_id = power_id)
    db.session.add(new_hero_power)
    db.session.commit()

    new_hero_power_dict = new_hero_power.to_dict()
    return make_response(jsonify(new_hero_power_dict), 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
