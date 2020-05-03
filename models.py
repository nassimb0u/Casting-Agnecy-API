from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from flask_migrate import Migrate
import os

database_uri = os.environ['DATABASE_URL']

db = SQLAlchemy()

# movie title max length
movie_title_length = int(os.environ.get('MOVIE_TITLE_LENGTH', 120))

# actor name max length
actor_name_length = int(os.environ.get('ACTOR_NAME_MAX_LENGTH', 60))

'''
ActionError Exception
A standardized way to communicate data integrity errors
'''
class ActionError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_uri=database_uri):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

# Movie
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(movie_title_length), unique=True, nullable=False)
    release_date = db.Column(db.DateTime(timezone=True), nullable=False)
    actors = db.relationship(
        'Assigning_actors_movies',
        backref='movies',
        lazy=True,
        cascade='save-update, delete'
    )

    def __init__(self, title=None, release_date=None, actors=[]):
        self.title = title
        self.release_date = release_date
        self.actors = actors

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        formatted_time = self.release_date.strftime('%d/%m/%Y %H:%M UTC%z')
        actors = [actor.actor_id for actor in self.actors]
        return {
            "id": self.id,
            "title": self.title,
            "release_date": formatted_time[0:-2],
            "actors": actors
        }    

#assigning actors and movies
class Assigning_actors_movies(db.Model):
    __tablename__ = 'actors_movies'
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    def __init__(self, actor_id=None, movie_id=None):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Actor
class Gender(Enum):
    male = 1
    female = 2

class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(actor_name_length), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable = False)
    movies = db.relationship(
        'Assigning_actors_movies',
        backref='actors',
        lazy=True,
        cascade='save-update, delete'
    )

    def __init__(self, name=None, age=None, gender=None, movies=[]):
        self.name = name
        self.age = age
        self.gender = gender
        self.movies = movies

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        movies = [movie.movie_id for movie in self.movies]
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender.name,
            "movies": movies
        }   


