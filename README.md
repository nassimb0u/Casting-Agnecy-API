# Casting Agency API

## Introduction

Casting Agency API is the Udacity Full Stack NanoDegree Capstone Project.

Casting Agency API models a company that is responsible for creating movies and managing and assigning actors to those movies.

## Motivation

This is the capstone project of Udacity Full Stack NanoDegree program, besides being indispensable for completing the nanodegree, it validates the obtained skills, in particular Flask, SQLAlchemy, Auth0, gunicorn and heroku to develop and deploy this RESTful API.

## Specifications

### Models:

* Movies with attributes title and release date
* Actors with attributes name, age and gender

## Endpoints:

* GET /actors and /movies
* DELETE /actors/ and /movies/
* POST /actors and /movies and
* PATCH /actors/ and /movies/

## Roles:

### Casting Assistant
* Can view actors and movies

### Casting Director
* All permissions a Casting Assistant has and…
* Add or delete an actor from the database
* Modify actors or movies

### Executive Producer
* All permissions a Casting Director has and…
* Add or delete a movie from the database

## Tests:

* One test for success behavior of each endpoint
* One test for error behavior of each endpoint
* At least two tests of RBAC for each role

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the python docs for [Unix](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) or [Windows](https://docs.python.org/3.8/using/windows.html).

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the postgres database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

The API was developped with SQLAlchemy ORM layer which provide a hight level of abstraction, so it can be configure to interact with many relational database management systems. Althoug we had used Postgresql for developpement and deployment, and we recommend it for testing the project.

- [PostgreSQL](https://www.postgresql.org/download/), also known as Postgres, is a free and open-source relational database management system (RDBMS).

## Database Setup

With Postgres server running, create a new database load the backup in `casting_agency.psql` provided file by running from the project directory:
```bash
createdb -U YOUR_USERNAME DATABASE_NAME
psql -U YOUR_USERNAME -d DATABASE_NAME < casting_agency.sql
```
You need to enter your password after each command(by defaul postgresql create a user postgres with password postgres).

## Running the server

Before running the server you need to personalize some environnement variables in `setup.sh` provided file:

```bash
DATABASE_URL=DIALECT+DRIVER://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
```

For example `postgresql://postgres:1717531@127.0.0.1:5432/casting_agency` for database `casting_agency` within postgres server running locally with default port 5432, user: postgres and password: 1717531

```
EXECUTIVE_PRODUCER_JWT, CASTING_DIRECTOR_JWT, CASTING_ASSISTANT_JWT
```

These variables are essential to successfully run the tests in `test_app.py` provided file, and they need to be updated with fresh JWTs in order to be authorized to interract with the API.

Besides running tests, JWTs are required to be included in requests headers as Bearer Token Authoriezation for all API endpoints.

```http headers
Authorization: Bearer YOUR_JWT
```

### How to update JWTs

To get or update JWTs for a specific role, log into my AUTH0 hosted page with the role corresponding user credentials:

* [here](https://nassimb.auth0.com/v2/logout?client_id=ceUmvORq0yEmLrhtaU9pCFuUXTKOo7fy&returnTo=https%3A%2F%2Fnassimb.auth0.com%2Fauthorize%3Faudience%3Dcasting_agency%26response_type%3Dtoken%26client_id%3DceUmvORq0yEmLrhtaU9pCFuUXTKOo7fy%26redirect_uri%3Dhttp%3A%2F%2Flocalhost%3A8080%2F) if you are running the API locally.

* [here](https://nassimb.auth0.com/v2/logout?client_id=ceUmvORq0yEmLrhtaU9pCFuUXTKOo7fy&returnTo=https%3A%2F%2Fnassimb.auth0.com%2Fauthorize%3Faudience%3Dcasting_agency%26response_type%3Dtoken%26client_id%3DceUmvORq0yEmLrhtaU9pCFuUXTKOo7fy%26redirect_uri%3Dhttps%3A%2F%2Fcasting-agency-api-nb.herokuapp.com%2F) if you are testing the live API on HEROKU.

#### Executive Producer
```
executiveproducer@castingagency.com
zWjRZXmrR439Dz2
```

#### Casting Director
```
castingdirector@castingagency.com
zWjRZXmrR439Dz2
```

#### Casting Assistant
```
castingassistant@castingagency.com
zWjRZXmrR439Dz2
```

### Running tests and the server

To run the tests, execute from the project directory:
```bash
source setup.sh
python test_app.py
```

Make sure you have internet connection, it is indispensable for validating JWTs with `AUTH0` public keys.

To run the server, from within the project directory directory, first ensure you are working using your created virtual environment, execute:

```bash
python app.py
```

## Demo Page

The API is hosted on [Heroku](https://dashboard.heroku.com/) and publically accessible with the following [link](https://casting-agency-api-nb.herokuapp.com/).

To test the hosted API or your local one with [Postman](https://www.postman.com/downloads/):

* Import the postman collection `./Capstone_project.postman_collection.json`
* Create an environement with the variable:

```bash
base_url=https://casting-agency-api-nb.herokuapp.com/
```

or if you would like to test your local API!

```bash
base_url=http://127.0.0.1:8080/
```

* Run the collection whitin the created environement.

## Endpoints Documentation

### `GET` '/movies'

Use this endpoint to fetche a list of all movies formatted as following:
```json
{
    "id": MOVIE_ID,
    "actors": LIST_OF_MOVIE_ACTORS_IDs,
    "release_date": MOVIE_RELEASE_DATE,
    "title": MOVIE_TITLE
}
``` 
#### Request Parameters:

None

#### Response Sample: 

Returns JSON data with movies informations.

```JSON
{
  "movies": [
    {
      "actors": [
          39
      ],
      "id": 6,
      "release_date": "24/04/2021 00:00 UTC+01",
      "title": "Movie"
    },
    {
      "actors": [
        35,
        39
      ],
      "id": 7,
      "release_date": "22/04/2020 00:00 UTC+01",
      "title": "Avengers"
    },
    {
      "actors": [],
      "id": 9,
      "release_date": "03/05/2021 00:00 UTC+01",
      "title": "Lion King"
    }
  ],
  "success": true,
  "total_movies": 3
}
```

### `GET` '/actors'

Use this endpoint to fetches a list of all actors formatted as follow:

```JSON
{
    "age": ACTOR_AGE,
    "gender": ACTOR_GENDER,
    "id": ACTOR_ID,
    "movies": LIST_OF_ACTOR_MOVIES_IDs,
    "name": ACTOR_NAME
}
```

#### Request Parameters:

None

#### Response Sample:

Returns JSON data with actors informations.

```JSON
{
  "actors": [
    {
      "age": 35,
      "gender": "male",
      "id": 43,
      "movies": [
        7
      ],
      "name": "Younes"
    },
    {
      "age": 39,
      "gender": "female",
      "id": 45,
      "movies": [
        9,
        7
      ],
      "name": "Amal"
    },
    {
      "age": 53,
      "gender": "male",
      "id": 48,
      "movies": [],
      "name": "Sahli"
    },
  ],
  "success": true,
  "total_actors": 3
}
```

### `DELETE` '/movies/<int:movie_id>'

Use this endpoint to delete the movie with the specified movie_id.

#### Request Parameters:

None

#### Response Sample:

Returns: Json data about the deleted movie id.

`/movies/9` may return:

```JSON
{
  "deleted": 9,
  "success": true
}
 ```

### `DELETE` '/actors/<int:actor_id>'

Use this endpoint to delete the actor with the specified actor_id.

#### Request Parameters:

None

#### Response Sample:

Returns JSON data about the deleted movie id.

`/actors/50` may return:

```JSON
{
  "deleted": 50,
  "success": true
}
 ```

### `POST` '/movies'

Use this endpoint to create a new movie.

#### Request Parameters:

```http post
title (Required): The title of the new movie (title must be unique)
release_date (Required): The new movie release date in the format "%d/%m/%Y %H:%M UTC%z"
actors: List of new movie actors IDs (referenced actors must already exist)
```

#### Rmarks

`release_date` format is "%d/%m/%Y %H:%M UTC%z" where:

* `%d`: Day of the month (01, 2, ... 31)
* `%m`: Month (1, 02, ... 12)
* `%Y`: Year
* `%H`: Hour, 24-hour clock
* `%M`: Minute (01, 2, 3, ... 59)
* `%z`: UTC offset in the form ±HH (+01, -04)

Exampeles:

* "22/04/2020 00:00 UTC+01"
* "3/5/2021 13:5 UTC-02"

#### Response Sample:

Returns JSON data, contains the ceated movie ID.

Request to this endpoint with the following data:

```JSON
{
	"title": "Avengers: Infinity War",
	"release_date": "23/04/2018 00:00 UTC+00",
	"actors": []
}
```

may return

```JSON
{
  "created": 11,
  "success": true
}
```

### `POST` '/actors'

Use this endpoint to create a new actor.

#### Request Parameters:

```http post
name (Required): The name of the new actor (name must be unique)
age (Required): The new actor age
gender (Required): actor's gender, accepts tow values `male` and `female`
movies: List of new actor movies IDs (referenced movies must already exist)
```

#### Response Sample:

Returns JSON data, contains the ID of the created actor.

Request to this endpoint with the following data:

```JSON
{
	"name": "actor",
	"age": 33,
	"gender": "male",
	"movies": [11, 10]
}
```

may return

```JSON
{
  "created": 57,
  "success": true
}
```

### `PATCH` '/movies/<int:movie_id>'

Use this endpoint to update an existant movie.

#### Request Parameters:

```http post
title: The new title of the movie (title must be unique)
release_date : The new release date of the movie in the format "%d/%m/%Y %H:%M UTC%z"
actors: The new list of movie actors IDs (referenced actors must already exist)
```

#### Response Sample:

Returns JSON data, contains the new informations of the updated movie.

Request to `/movies/10` with the following data:

```JSON
{
	"release_date": "4/5/2020 7:13 UTC+01"
}
```

may return

```JSON
{
  "success": true,
  "updated": {
    "actors": [
      55
    ],
    "id": 10,
    "release_date": "04/05/2020 07:13 UTC+01",
    "title": "movie 5857"
  }
}
```

or if the new informations matche the old:

```JSON
{
  "success": true,
  "updated": "unchanged"
}

```

### `PATCH` '/actors/<int:actor_id>'

Use this endpoint to update an existant actor.

#### Request Parameters:

```http post
name: The new name of the actor (name must be unique)
age: The new age of the actor
gender: The correct gender of the actor, you may made typos
movies: The new list of actor movies IDs (referenced movies must already exist)
```

#### Response Sample:

Returns JSON data, contains the new informations of the updated actor.

Request to `/actors/45` with the following data:

```JSON
{
	"age": 20,
}
```

may return:

```JSON
{
  "success": true,
  "updated": {
    "age": 20,
    "gender": "male",
    "id": 45,
    "movies": [
      7
    ],
    "name": "Channing Tatum"
  }
}
```

or if the new informations matche the old:

```JSON
{
  "success": true,
  "updated": "unchanged"
}
```

### Errors

##### Standard Error Responses

`400`
```JSON
{
    "success": false,
    "status": 400,
    "message": "bad request"
}
```

`404`
```JSON
{
    "success": false,
    "status": 404,
    "message": "resource not found"
}
```

`405`
```JSON
{
    "success": false,
    "status": 405,
    "message": "The method is not allowed for the requested URL"
}
```



`422`
```JSON
{
    "success": false,
    "status": 422,
    "message": "unprocessable"
}
```

`500`
```JSON
{
    "success": false,
    "status": 500,
    "message": "internal server error"
}
```

#### `POST` '/actors'

```JSON
{
    "success": false,
    "status": 422,
    "message": {
        "error": "missing actor informations",
        "description": "PARAMETER_NAME is required"
    }
}
```
The required parameters were not sent in the request

```JSON
{
    "success": false,
    "status": 422,
    "message": {
        "error": "integrity error",
        "description": "Referenced movie[s] does not exist in the database, confim their ids before assign to actor"
    }
}
```

```JSON
{
    "success": false,
    "status": 422,
    "message": {
        "error": "integrity error",
        "description": "Duplicated actor name"
    }
}
```


#### `POST` '/movies'

Same as for `POST` '/actors'




