import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from datetime import datetime
from auth import AuthError, requires_auth

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
  @requires_auth('get:actors')
  def get_actors(payload):
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
  @requires_auth('get:movies')
  def get_movies(payload):
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
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
    movie = Movie.query.get(movie_id)
    if movie is None:
      abort(404)
    movie.delete()
    return jsonify({
      'success': True,
      'deleted': movie_id
    })
  
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
      abort(404)
    actor.delete()
    return jsonify({
      'success': True,
      'deleted': actor_id
    })
  
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(payload):
    try:
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)
    except:
      abort(400)
    try:
      if age < 18 or age > 100: raise Exception('age should belong to [18;100]')
      new_actor = Actor(name, age, gender)
      new_actor.insert()
      return jsonify({
        'success': True,
        'created': new_actor.id
      })
    except:
      abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(payload):
    try:
      body = request.get_json()
      title = body.get('title', None)
      release_date = body.get('release_date', None)
      release_date += '00'
      dt_realease_date = datetime.strptime(release_date, '%d/%m/%Y %H:%M %z')
    except:
      abort(400)
    try:
      new_movie = Movie(title, release_date)
      new_movie.insert()
      return jsonify({
        'success': True,
        'created': new_movie.id
      })
    except:
      abort(422)
  
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
      abort(404)
    try:
      updated = False
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)
      if name is not None and actor.name != name:
         actor.name = name
         updated = True
      if age is not None and actor.age != age:
        if age < 18 or age > 100: raise Exception('age should belong to [18;100]')
        actor.age = age
        updated = True
      if gender is not None and actor.gender.name != gender: 
        actor.gender = gender
        updated = True
    except:
      abort(400)
    try:
      if updated: actor.update()
      return jsonify({
        'success': True,
        'updated': actor.format() if updated else 'unchanged'
      })
    except:
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, movie_id):
    movie = Movie.query.get(movie_id)
    if movie is None:
      abort(404)
    try:
      updated = False
      body = request.get_json()
      title = body.get('title', None)
      release_date = body.get('release_date', None)
      if release_date is not None:
        release_date += '00'
        dt_realease_date = datetime.strptime(release_date, '%d/%m/%Y %H:%M UTC%z')
        if dt_realease_date != movie.release_date:
          movie.release_date = dt_realease_date
          updated = True
      if title is not None and title != movie.title: 
        movie.title = title
        updated = True
    except:
      abort(400)
    try:
      if updated: movie.update()
      return jsonify({
        'success': True,
        'updated': movie.format() if updated else 'unchanged'
      })
    except:
      abort(422)

  '''
  Create error handlers for all expected errors
	'''
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404
    
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400
  
  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal server error"
    }), 500
  
  @app.errorhandler(AuthError)
  def handle_authError(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)