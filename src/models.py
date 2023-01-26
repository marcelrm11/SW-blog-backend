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

class Character_X_Vehicle(db.Model):
    __tablename__ = 'character_x_vehicle'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    characters = db.relationship('Character', backref='character_x_vehicle')
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    vehicles = db.relationship('Vehicle', backref='character_x_vehicle')

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