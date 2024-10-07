from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # Relationship mapping the hero to related hero_powers
    hero_powers = db.relationship(
        'HeroPower', back_populates='hero', cascade='all, delete-orphan')
    
    # Association proxy to get powers for this hero through hero_powers
    powers = association_proxy('hero_powers', 'power',
                                 creator=lambda power_obj: HeroPower(power=power_obj))
    
    serialize_rules = ('-hero_powers.hero',)

    def __repr__(self):
        return f'<Hero id: {self.id}, name: {self.name}, super_name: {self.super_name}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    
    # Relationship mapping the power to related hero_powers
    hero_powers = db.relationship(
        'HeroPower', back_populates='power',cascade='all, delete-orphan')

    # Association proxy to get hero for this project through hero_powers
    heroes = association_proxy('hero_powers', 'hero',
                                  creator=lambda hero_obj: HeroPower(hero=hero_obj))

    serialize_rules = ('-hero_powers.power',)

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description must be present and should be at least 20 characters long")
        return description

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
    
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers',)

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength.title() not in valid_strengths:
            raise ValueError(f"Strength must be one of the following values: {', '.join(valid_strengths)}")
        return strength

    def __repr__(self):
        return f'<HeroPower id: {self.id}, strength: {self.strength}, hero_id: {self.hero_id}, power_id: {self.power_id}>'