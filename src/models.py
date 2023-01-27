from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(120))
    favorites = db.relationship('Favorite', backref='user')

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    url = db.Column(db.String(240), unique=True)
    diameter_in_km = db.Column(db.Float)
    rotation_period_in_days = db.Column(db.Float)
    orbital_period_in_days = db.Column(db.Float)
    gravity_in_g = db.Column(db.Float)
    population = db.Column(db.Integer)
    climate = db.Column(db.String(240)) 
    terrain = db.Column(db.String(240)) 
    surface_water_percent = db.Column(db.Float)
    characters = db.relationship('Character', backref='planet', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "diameter_in_km": self.diameter_in_km,
            "rotation_period_in_days": self.rotation_period_in_days,
            "orbital_period_in_days": self.orbital_period_in_days,
            "gravity_in_g": self.gravity_in_g,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water_percent": self.surface_water_percent
        }

    def __repr__(self):
        return f'<Planet ID: {self.id}, name: {self.name}>'


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    url = db.Column(db.String(240), unique=True)
    model = db.Column(db.String(150))
    vehicle_class = db.Column(db.String(150))
    manufacturer = db.Column(db.String(150))
    cost_in_credits = db.Column(db.Float)
    length_in_m = db.Column(db.Float)
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    max_atmosphering_speed_in_kmh = db.Column(db.Float)
    cargo_capacity_in_kg = db.Column(db.Float)
    characters = db.relationship('Character_X_Vehicle', backref='vehicle')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length_in_m": self.length_in_m,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed_in_kmh": self.max_atmosphering_speed_in_kmh,
            "cargo_capacity_in_kg": self.cargo_capacity_in_kg,
            "characters": [character.serialize() for character in self.characters]
        }

    def __repr__(self):
        return f'<Character ID: {self.id}, name: {self.name}>'


class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    url = db.Column(db.String(240), unique=True)
    height_in_cm = db.Column(db.Float)
    mass_in_kg = db.Column(db.Float)
    hair_color = db.Column(db.String(30))
    skin_color = db.Column(db.String(30))
    eye_color = db.Column(db.String(30))
    birthyear = db.Column(db.String(30))
    gender = db.Column(db.String(30))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    vehicles = db.relationship('Character_X_Vehicle', backref='character')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "height_in_cm": self.height_in_cm,
            "mass_in_kg": self.mass_in_kg,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birthyear": self.birthyear,
            "gender": self.gender,
            "planet_id": self.planet_id,
            "vehicles": [vehicle.serialize() for vehicle in self.vehicles]
        }

    def __repr__(self):
        return f'<Character ID: {self.id}, name: {self.name}>'

class Character_X_Vehicle(db.Model):
    __tablename__ = 'character_x_vehicle'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship('Character', backref='characters_vehicles')
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    vehicle = db.relationship('Vehicle', backref='characters_vehicles')

    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            "character": self.character.serialize(),
            "vehicle_id": self.vehicle_id,
            "vehicle": self.vehicle.serialize()
        }
    

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    characters = db.relationship('Character', backref='favorite')
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planets = db.relationship('Planet', backref='favorite')
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    vehicles = db.relationship('Vehicle', backref='favorite')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }