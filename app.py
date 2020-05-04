import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Movie, Actor, ActionError, Assigning_actors_movies, Gender
from datetime import datetime
from auth import AuthError, requires_auth
from sqlalchemy.exc import IntegrityError
from endpoints_errors import verify_actor_submitted_info, no_actor_error, no_movie_error
from endpoints_errors import verify_movie_submitted_info, movie_release_date_error

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
      raise no_actor_error
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
      raise no_movie_error
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
    except:
      abort(400)
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')
    movies = body.get('movies', [])
    movies = verify_actor_submitted_info(name, age, gender, movies)
    if gender.lower() != 'male': gender = Gender.female
    else: gender = Gender.male
    new_actor = Actor(name, age, gender, movies)
    attributes = vars(new_actor)
    for couple in attributes.items():
      if couple[1] is None:
        raise ActionError({
        'error': 'missing actor informations',
        'description': '`%s` is required'%couple[0]
        }, 422)
    try:
      new_actor.insert()
      return jsonify({
        'success': True,
        'created': new_actor.id
      })
    except IntegrityError as e:
      if 'unique constraint' in str(e.orig):
        description = 'Duplicated actor name, actor `%s` alrady exists'%name
      elif 'foreign key constraint' in str(e.orig):
        description = 'Referenced movie[s] does not exist in the database, \
confim their ids before assign to actor'
      raise ActionError({
      'error': 'integrity error',
      'description': description
      }, 422)
    except:
      abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(payload):
    try:
      body = request.get_json()
    except:
      abort(400)
    title = body.get('title')
    release_date = body.get('release_date')
    actors = body.get('actors', [])
    actors = verify_movie_submitted_info(title, release_date, actors)
    release_date += '00'
    try:
      dt_realease_date = datetime.strptime(release_date, '%d/%m/%Y %H:%M UTC%z')
    except:
      raise movie_release_date_error
    new_movie = Movie(title, dt_realease_date, actors)
    attributes = vars(new_movie)
    for couple in attributes.items():
      if couple[1] is None:
        raise ActionError({
        'error': 'missing movie informations',
        'description': '`%s` is required'%couple[0]
        }, 422)
    try:
      new_movie.insert()
      return jsonify({
        'success': True,
        'created': new_movie.id
      })
    except IntegrityError as e:
      if 'unique constraint' in str(e.orig):
        description = 'Duplicated movie title, movie `%s` alrady exists'%title
      elif 'foreign key constraint' in str(e.orig):
        description = 'Referenced actor[s] does not exist in the database, \
confim their ids before assign to movie'
      raise ActionError({
      'error': 'integrity error',
      'description': description
      }, 422)
    except:
      abort(422)
  
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
      abort(404)
    try:
      body = request.get_json()
    except:
      abort(400)
    updated = False
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')
    movies = body.get('movies')
    actors_movies = verify_actor_submitted_info(name, age, gender, movies)
    if name is not None and actor.name != name:
      actor.name = name
      updated = True
    if age is not None and actor.age != age:
      actor.age = age
      updated = True
    if gender is not None and actor.gender.name != gender: 
      actor.gender = gender
      updated = True
    if movies is not None and [actor_movie.movie_id for actor_movie in actor.movies] != movies:
      actor.movies = actors_movies
      updated = True
    try:
      if updated: actor.update()
      return jsonify({
        'success': True,
        'updated': actor.format() if updated else 'unchanged'
      })
    except IntegrityError as e:
      if 'unique constraint' in str(e.orig):
        description = 'Duplicated actor name, actor `%s` alrady exists'%name
      elif 'foreign key constraint' in str(e.orig):
        description = 'Referenced movie[s] does not exist in the database, \
confim their ids before assign to actor'
      raise ActionError({
      'error': 'integrity error',
      'description': description
      }, 422)
    except:
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, movie_id):
    movie = Movie.query.get(movie_id)
    if movie is None:
      abort(404)
    try:
      body = request.get_json()
    except:
      abort(400)
    updated = False
    title = body.get('title')
    release_date = body.get('release_date')
    actors = body.get('actors')
    actors_movies = verify_movie_submitted_info(title, release_date, actors)
    if release_date is not None:
      release_date += '00'
      dt_realease_date = datetime.strptime(release_date, '%d/%m/%Y %H:%M UTC%z')
      if dt_realease_date != movie.release_date:
        movie.release_date = dt_realease_date
        updated = True
    if title is not None and title != movie.title: 
      movie.title = title
      updated = True
    if actors is not None and [actor_movie.actor_id for actor_movie in movie.actors] != actors:
      movie.actors = actors_movies
      updated = True
    try:
      if updated: movie.update()
      return jsonify({
        'success': True,
        'updated': movie.format() if updated else 'unchanged'
      })
    except IntegrityError as e:
      if 'unique constraint' in str(e.orig):
        description = 'Duplicated movie title, movie `%s` alrady exists'%title
      elif 'foreign key constraint' in str(e.orig):
        description = 'Referenced actor[s] does not exist in the database, \
confim their ids before assign to movie'
      raise ActionError({
      'error': 'integrity error',
      'description': description
      }, 422)
    except:
      abort(422)

  '''
  Create error handlers for all expected errors
	'''
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "status": 404,
      "message": "resource not found"
    }), 404
    
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "status": 422,
      "message": "unprocessable"
    }), 422
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "status": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(405)
  def bad_request(error):
    return jsonify({
      "success": False,
      "status": 405,
      "message": "The method is not allowed for the requested URL"
    }), 405
  
  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False,
      "status": 500,
      "message": "internal server error"
    }), 500
  
  @app.errorhandler(AuthError)
  def handle_authError(error):
    return jsonify({
        'success': False,
        'status': error.status_code,
        'message': error.error
    }), error.status_code
  
  @app.errorhandler(ActionError)
  def handle_actionError(error):
    return jsonify({
        'success': False,
        'status': error.status_code,
        'message': error.error
    }), error.status_code

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)