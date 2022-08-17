from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

pilots_table = db.Table(
    "character_vehicle",
   db.Column("character_id", db.ForeignKey("character.id"), primary_key=True),
   db.Column("vehicle_id", db.ForeignKey("vehicle.id"), primary_key=True),
)

films_characters_table = db.Table(
    "film_character",
   db.Column("film_id", db.ForeignKey("film.id"), primary_key=True),
   db.Column("character_id", db.ForeignKey("character.id"), primary_key=True),
)

films_planets_table = db.Table(
    "film_planet",
   db.Column("film_id", db.ForeignKey("film.id"), primary_key=True),
   db.Column("planet_id", db.ForeignKey("planet.id"), primary_key=True),
)

films_vehicles_table = db.Table(
    "film_vehicle",
   db.Column("film_id", db.ForeignKey("film.id"), primary_key=True),
   db.Column("vehicle_id", db.ForeignKey("vehicle.id"), primary_key=True),
)

favs_characters = db.Table(
    "user_character",
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True),
    db.Column("character_id", db.ForeignKey("character.id"), primary_key=True)
)

favs_planets = db.Table(
    "user_planet",
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True),
    db.Column("planet_id", db.ForeignKey("planet.id"), primary_key=True)
)
favs_vehicles = db.Table(
    "user_vehicle",
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True),
    db.Column("vehicle_id", db.ForeignKey("vehicle.id"), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id =db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String(50), nullable=False)
    email =db.Column(db.String(150), nullable=False, unique=True)
    favs_characters_id = db.relationship('Character', secondary=favs_characters, lazy="subquery", backref=db.backref("users", lazy=True))
    favs_planets_id = db.relationship('Planet', secondary=favs_planets, lazy="subquery", backref=db.backref("users", lazy=True))
    favs_vehicles_id = db.relationship('Vehicle', secondary=favs_vehicles, lazy="subquery", backref=db.backref("users", lazy=True))
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "favs_characters": [character.serialize() for character in self.favs_characters_id] if self.favs_characters_id else [],
            "favs_planets": [planet.serialize() for planet in self.favs_planets_id] if self.favs_planets_id else [],
            "favs_vehicles": [vehicle.serialize() for vehicle in self.favs_vehicles_id] if self.favs_planets_id else []
        }


class Character(db.Model):
    __tablename__ = 'character'
    id =db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(50), nullable=False)
    hair_color =db.Column(db.String(50))
    birth_year =db.Column(db.String(10))
    homeworld_id =db.Column(db.Integer, db.ForeignKey("planet.id"))
    homeworld =db.relationship("Planet", backref=db.backref("character", uselist=False))
    vehicles =db.relationship(
        "Vehicle", secondary=pilots_table, backref="pilots"
    )
    url =db.Column(db.String(200), nullable=False, unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "birth_year": self.birth_year,
            "homeworld": self.homeworld.name if self.homeworld else "Unknow",
            "url":self.url
        }


class Planet(db.Model):
    __tablename__ = 'planet'
    id =db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(50), nullable=False)
    diameter =db.Column(db.Integer)
    population =db.Column(db.Integer)
    url =db.Column(db.String(200), nullable=False, unique=True)
    
    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "diameter":self.diameter,
            "population":self.population,
            "url":self.url
        }


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id =db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(50), nullable=False)
    model =db.Column(db.String(50))
    cost_in_credits =db.Column(db.String(50))
    vehicle_class =db.Column(db.String(50))
    url =db.Column(db.String(200), nullable=False, unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "cost_in_credits": self.cost_in_credits,
            "vehicle_class": self.vehicle_class,
            "url" : self.url
        }

class Film(db.Model):
    __tablename__ = 'film'
    id =db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(50), nullable=False)
    episode_id =db.Column(db.Integer, nullable=False)
    director =db.Column(db.String(50))
    characters = db.relationship(
        "Character", secondary=films_characters_table, lazy='subquery', backref=db.backref('films', lazy=True)
    )
    planets =db.relationship(
        "Planet", secondary=films_planets_table, lazy='subquery', backref=db.backref('films', lazy=True)
    )
    vehicles =db.relationship(
        "Vehicle", secondary=films_vehicles_table, lazy='subquery', backref=db.backref('films', lazy=True)
    )
    url =db.Column(db.String(200), nullable=False, unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "episode": self.episode_id,
            "director": self.director,
            "url" : self.url
        }