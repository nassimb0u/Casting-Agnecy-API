from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from flask_migrate import Migrate

database_name = "casting_agency"
database_uri = "postgres://{}:{}@{}/{}".format("postgres","1717531","127.0.0.1:5432",database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_uri=database_uri):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    #db.create_all()

# Movie
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    actors = db.relationship('Assigning_actors_movies', backref='movies', lazy=True, cascade='delete')

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "title": self.title,
            "release_date": self.release_date 
        }    

#assigning actors and movies
class Assigning_actors_movies(db.Model):
    __tablename__ = 'actors_movies'
    id = db.Column(db.Integer, primary_key=True)
    actor = db.Column(db.String(60), db.ForeignKey('actors.name'), nullable=False)
    movie = db.Column(db.String(120), db.ForeignKey('movies.title'), nullable=False)

    def __init__(self, actor, movie):
        self.actor = actor
        self.movie = movie

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
    name = db.Column(db.String(60), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable = False)
    movies = db.relationship('Assigning_actors_movies', backref='actors', lazy=True, cascade='delete')

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender.name
        }   


