import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from datetime import datetime

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers',
      'Content-Type, Authorization'
      )
    response.headers.add(
      'Access-Control-Allow-Methods', 
      'GET, PATCH, POST, DELETE'
      )
    return response

  @app.route('/')
  def test():
    return 'healty'
  
  @app.route('/actors')
  def get_actors():
    actors = Actor.query.order_by('id').all()
    if len(actors) == 0:
      abort(404)
    formatted_actors = [actor.format() for actor in actors]
    return jsonify({
      'success': True,
      'actors': formatted_actors,
      'total_actors': len(formatted_actors)
    })
  
  @app.route('/movies')
  def get_movies():
    movies = Movie.query.order_by('id').all()
    if len(movies) == 0:
      abort(404)
    formatted_movies = [movie.format() for movie in movies]
    return jsonify({
      'success': True,
      'movies': formatted_movies,
      'total_movies': len(formatted_movies)
    })
  
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie is None:
      abort(404)
    movie.delete()
    return jsonify({
      'success': True,
      'deleted': movie_id
    })
  
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
      abort(404)
    actor.delete()
    return jsonify({
      'success': True,
      'deleted': actor_id
    })
  
  @app.route('/actors', methods=['POST'])
  def create_actor():
    try:
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)
      new_actor = Actor(name, age, gender)
      new_actor.insert()
      return jsonify({
        'success': True,
        'created': new_actor.id
      })
    except:
      abort(400)

  @app.route('/movies', methods=['POST'])
  def create_movie():
    try:
      body = request.get_json()
      title = body.get('title', None)
      release_date = body.get('release_date', None)
      release_date += '00'
      dt_realease_date = datetime.strptime(release_date, '%d/%m/%Y %H:%M %z')
      new_movie = Movie(title, release_date)
      new_movie.insert()
      return jsonify({
        'success': True,
        'created': new_movie.id
      })
    except:
      abort(400)
  
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  def update_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
      abort(404)
    try:
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)
      if name is not None: actor.name = name
      if age is not None: actor.age = age
      if gender is not None actor.gender = gender
      actor.update
      return jsonify({
        'success': True,
        'updated': actor.format()
      })
    except:
      abort(400)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  def update_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie is None:
      abort(404)
    try:
      body = request.get_json()
      title = body.get('title', None)
      release_date = body.get('release_date', None)
      if release_date is not None:
        release_date += '00'
        dt_realease_date = datetime.strptime(release_date, '%d/%m/%Y %H:%M %z')
        movie.release_date = dt_realease_date
      if title is not None: movie.title = title
      movie.update
      return jsonify({
        'success': True,
        'updated': movie.format()
      })
    except:
      abort(400)
  

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)