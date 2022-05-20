from datetime import date

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import MoviesModel, GenresModel, MovieGenreModel, ActorsModel, CastModel
from constants import OFFSET_DEFAULT, LIMIT_DEFAULT
from app.decorators import admin_group_required

movies_bp = Blueprint('movies', __name__)


@movies_bp.route("/movies/", methods=["GET"])
def get_movies():
    name = request.args.get("name")
    director_id = request.args.get("director_id")
    offset = request.args.get("offset", OFFSET_DEFAULT)
    limit = request.args.get("limit", LIMIT_DEFAULT)

    if name:
        movies = MoviesModel.find_by_name(name)
    elif director_id:
        movies = MoviesModel.find_by_director_id(director_id, offset, limit)
    else:
        movies = MoviesModel.return_all(offset, limit)

    return jsonify(movies)


@movies_bp.route("/movies/<int:id>", methods=["GET"])
def get_movie(id):
    movie = MoviesModel.find_by_id(id)
    if not movie:
        return jsonify({"message": "Movie not found."}), 404

    return jsonify(movie)


@movies_bp.route("/movies", methods=["POST"])
@jwt_required()
@admin_group_required
def create_movie():
    if not request.json:
        return jsonify({"message": 'Please, specify "name", "description", "release_date(year, month, day)", '
                                   '"director_id", "genres"(list) and "actors"(list).'}), 400

    name = request.json.get("name")
    description = request.json.get("description")
    year = request.json.get("year")
    month = request.json.get("month")
    day = request.json.get("day")
    director_id = request.json.get("director_id")
    genres = request.json.get("genres")
    actors = request.json.get("actors")

    if not name or not description or not year or not month or \
            not day or not director_id or not genres or not actors:
        return jsonify({"message": 'Please, specify name, description, '
                                   'year, month, day, director_id, genres and actors.'}), 400
    movie = MoviesModel(name=name, description=description,
                        release_date=date(year=int(year), month=int(month), day=int(day)), director_id=director_id)
    movie.save_to_db()

    for genre in genres:
        adding_genre = GenresModel.find_by_genre(genre, to_dict=False)
        adding_movie_genre = MovieGenreModel(movie_id=movie.id, genre_id=adding_genre.id)
        adding_movie_genre.save_to_db()

    for actor in actors:
        firstname, lastname = actor.split()
        adding_actor = ActorsModel.find_by_name(firstname, lastname, to_dict=False)
        adding_cast = CastModel(movie_id=movie.id, actor_id=adding_actor.id)
        adding_cast.save_to_db()

    return jsonify({"id": movie.id}), 201


@movies_bp.route("/movies/<int:id>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def update_movie(id):
    name = request.json.get("name")
    description = request.json.get("description")
    year = request.json.get("year")
    month = request.json.get("month")
    day = request.json.get("day")
    director_id = request.json.get("director_id")
    genres = request.json.get("genres")
    actors = request.json.get("actors")

    movie = MoviesModel.find_by_id(id, to_dict=False)
    if not movie:
        return jsonify({"message": "Movie not found."}), 404

    if name:
        movie.name = name
    if description:
        movie.description = description
    if year:
        movie.release_date = movie.release_date.replace(year=year)
    if month:
        movie.release_date = movie.release_date.replace(month=month)
    if day:
        movie.release_date = movie.release_date.replace(day=day)
    if director_id:
        movie.director_id = director_id

    if genres:
        for genre in genres:
            adding_genre = GenresModel.find_by_genre(genre, to_dict=False)
            search_movie_genre = MovieGenreModel.find_by_ids(movie_id=movie.id, genre_id=adding_genre.id)
            if search_movie_genre:
                continue
            adding_movie_genre = MovieGenreModel(movie_id=movie.id, genre_id=adding_genre.id)
            adding_movie_genre.save_to_db()

    if actors:
        for actor in actors:
            firstname, lastname = actor.split()
            adding_actor = ActorsModel.find_by_name(firstname, lastname, to_dict=False)
            search_cast = CastModel.find_by_ids(movie_id=movie.id, actor_id=adding_actor.id)
            if search_cast:
                continue
            adding_cast = CastModel(movie_id=movie.id, actor_id=adding_actor.id)
            adding_cast.save_to_db()
    movie.save_to_db()

    return jsonify({"message": "Updated"})


@movies_bp.route("/movies/changes/<int:id>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def delete_genre_or_cast(id):

    movie = MoviesModel.find_by_id(id, to_dict=False)
    if not movie:
        return jsonify({"message": "Movie not found."}), 404

    genres = request.json.get("genres")
    actors = request.json.get("actors")
    result = {}
    if genres:
        for genre in genres:
            adding_genre = GenresModel.find_by_genre(genre, to_dict=False)
            search_movie_genre = MovieGenreModel.find_by_ids(movie_id=movie.id, genre_id=adding_genre.id)
            res = MovieGenreModel.delete(search_movie_genre)
            if res == 404:
                result[genre] = "Not Found"
            else:
                result[genre] = "Deleted"
    if actors:
        for actor in actors:
            firstname, lastname = actor.split()
            adding_actor = ActorsModel.find_by_name(firstname, lastname, to_dict=False)
            search_cast = CastModel.find_by_ids(movie_id=movie.id, actor_id=adding_actor.id)
            res = CastModel.delete(search_cast)
            if res == 404:
                result[actor] = "Not Found"
            else:
                result[actor] = "Deleted"
    return jsonify(result)


@movies_bp.route("/movies/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_group_required
def delete_movie(id):
    movie = MoviesModel.delete_by_id(id)
    if movie == 404:
        return jsonify({"message": "Movie not found."}), 404
    return jsonify({"message": "Deleted"})
