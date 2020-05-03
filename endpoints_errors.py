from models import ActionError, Assigning_actors_movies
from models import actor_name_length, movie_title_length

'''
endpoints actions common errors
'''
no_actor_error = ActionError({
        'error': 'resource not found',
        'description': 'No actor was found in the database'
      }, 404)

no_movie_error = ActionError({
        'error': 'resource not found',
        'description': 'No movie was found in the database'
      }, 404)

actor_age_error = ActionError({
      'error': 'invalide actor informations',
      'description': '`age` must be an integer in the interval [18;100], no child labour :3'
      }, 422)

actor_gender_error = ActionError({
      'error': 'invalide actor informations',
      'description': '`gender` accepts only two values `male` and `female`'
      }, 422)

actor_name_error = ActionError({
      'error': 'invalide actor informations',
      'description': '`name` must be string less than %s char'% str(actor_name_length)
      }, 422)

actor_movies_error = ActionError({
        'error': 'invalide actor informations',
        'description': '`movies` should contains list of movies integer ids'
        }, 422)

movie_title_error = ActionError({
        'error': 'invalide movie informations',
        'description': '`title`  must be string less than %s char'% str(movie_title_length)
        }, 422)

movie_actors_error = ActionError({
        'error': 'invalide actor informations',
        'description': '`actors` should contains list of actors integer ids'
        }, 422)

movie_release_date_error = ActionError({
        'error': 'invalide actor informations',
        'description': '`release_date` malformatted'
        }, 422)



# verify actor submitted informations
def verify_actor_submitted_info(name, age, gender, movies):
    if name is not None and (type(name) != str or len(name) > actor_name_length):
        raise actor_name_error
    if age is not None and (type(age) != int or age < 18 or age > 100):
        raise actor_age_error
    if gender is not None and (type(gender) != str or gender.lower() not in ['male', 'female']):
        raise actor_gender_error
    actors_movies = []
    if movies is not None:
        if type(movies) != list: raise actor_movies_error
        for movie_id in movies:
            if type(movie_id) != int:
                raise actor_movies_error
            actors_movies.append(Assigning_actors_movies(movie_id=movie_id))
    return actors_movies

# verify movie submitted informations
def verify_movie_submitted_info(title, release_date, actors):
    if title is not None and (type(title) != str or len(title) > movie_title_length):
        raise movie_title_error
    long_datetime = '02/05/2020 22:33 UTC+01'
    short_datetime= '2/5/2020 4:3 UTC+01'
    if release_date is not None:
        if( type(release_date) != str or len(release_date) > len(long_datetime)
            or len(release_date) < len(short_datetime) ):
            raise movie_release_date_error
    actors_movies = []
    if actors is not None:
        if type(actors) != list: raise movie_actors_error
        for actor_id in actors:
            if type(actor_id) != int:
                raise movie_actors_error
            actors_movies.append(Assigning_actors_movies(actor_id=actor_id))
    return actors_movies