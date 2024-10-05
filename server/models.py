from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # Relationship mapping the employee to related assignments
    hero_powers = db.relationship(
        'HeroPower', back_populates='hero', cascade='all, delete-orphan')
    
    # Association proxy to get projects for this employee through assignments
    powers = association_proxy('hero_powers', 'power',
                                 creator=lambda power_obj: Assignment(power=power_obj))

    def __repr__(self):
        return f'<Hero id: {self.id}, name: {self.name}, super_name: {self.super_name}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    
    # Relationship mapping the project to related assignments
    hero_powers = db.relationship(
        'HeroPower', back_populates='power',cascade='all, delete-orphan')

    # Association proxy to get employees for this project through assignments
    heroes = association_proxy('hero_powers', 'hero',
                                  creator=lambda hero_obj: Assignment(hero=hero_obj))

    def __repr__(self):
        return f'<Power id: {self.id}, name: {self.name}, description: {self.description}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)

    # Foreign key to store the hero id
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    # Foreign key to store the power id
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    # Relationship mapping the heropower to related hero
    hero = db.relationship('Hero', back_populates='hero_powers')
    # Relationship mapping the heropower to related power
    power = db.relationship('Power', back_populates='hero_powers')

    def __repr__(self):
        return f'<HeroPower id: {self.id}, strength: {self.strength}, hero_id: {self.hero_id}, power_id: {self.power_id}>'