from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime, Integer
from enum import Enum

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
    db.create_all()

# Movie
class Movie(db.Model):
    __tablename__ = 'movies'
    title = Column(String(120), primary_key=True)
    release_date = Column(DateTime, nullable=False)

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


# Actor
class Gender(Enum):
    male = 1
    female = 2

class Actor(db.Model):
    __tablename__ = 'actors'
    name = Column(String(60), parimary_key=True)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(Gender), nullable = False)

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


