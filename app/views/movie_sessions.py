from datetime import datetime

from flask import jsonify, request, Blueprint

from app.models import MovieSessionsModel, AuditoriumModel
from constants import OFFSET_DEFAULT, LIMIT_DEFAULT

movie_sessions_bp = Blueprint('sessions', __name__)


@movie_sessions_bp.route("/sessions/", methods=["GET"])
def get_movie_sessions():
    movie_id = request.args.get("movie_id")
    auditorium_id = request.args.get("auditorium_id")
    left_date = request.json.get("left_date")
    right_date = request.json.get("right_date")

    if movie_id:
        movie_sessions = MovieSessionsModel.find_by_movie_id(movie_id, OFFSET_DEFAULT, LIMIT_DEFAULT)
    elif auditorium_id:
        movie_sessions = MovieSessionsModel.find_by_auditorium_id(auditorium_id, OFFSET_DEFAULT, LIMIT_DEFAULT)
    elif left_date and right_date:
        left_date = datetime(*list(left_date))
        right_date = datetime(*list(right_date))
        movie_sessions = MovieSessionsModel.find_by_dates(left_date, right_date, OFFSET_DEFAULT, LIMIT_DEFAULT)
    else:
        movie_sessions = MovieSessionsModel.return_all(OFFSET_DEFAULT, LIMIT_DEFAULT)

    return jsonify(movie_sessions)


@movie_sessions_bp.route("/sessions/<int:id>", methods=["GET"])
def get_movie_session(id):
    movie_session = MovieSessionsModel.find_by_id(id)
    if not movie_session:
        return jsonify({"message": "Movie session not found."}), 404

    return jsonify(movie_session)


@movie_sessions_bp.route("/sessions", methods=["POST"])
def create_movie_session():
    if not request.json:
        return jsonify({"message": 'Please, specify "movie_id", "auditorium_id", '
                                   '"release_date(year, month, day, hour, minute)"'}), 400

    movie_id = request.json.get("movie_id")
    auditorium_id = request.json.get("auditorium_id")
    year = request.json.get("year")
    month = request.json.get("month")
    day = request.json.get("day")
    hour = request.json.get("hour")
    minute = request.json.get("minute")

    if not movie_id or not auditorium_id or not year or not month or \
            not day or not isinstance(hour, int) or not isinstance(minute, int):
        return jsonify({"message": 'Please, specify movie_id, auditorium_id, '
                                   'year, month, day, hour minute.'}), 400
    session_date = datetime(year=int(year), month=int(month), day=int(day))
    session_date = session_date.replace(hour=int(hour), minute=int(minute))
    movie_session = MovieSessionsModel(movie_id=movie_id, auditorium_id=auditorium_id,
                                       date=session_date,
                                       remain_seats=AuditoriumModel.find_by_id(auditorium_id, to_dict=False).seats)
    movie_session.save_to_db()

    return jsonify({"id": movie_session.id}), 201


@movie_sessions_bp.route("/sessions/<int:id>", methods=["PATCH"])
def update_movie_session(id):
    movie_id = request.json.get("movie_id")
    auditorium_id = request.json.get("auditorium_id")
    year = request.json.get("year")
    month = request.json.get("month")
    day = request.json.get("day")
    hour = request.json.get("hour")
    minute = request.json.get("minute")

    movie_session = MovieSessionsModel.find_by_id(id, to_dict=False)
    if not movie_session:
        return jsonify({"message": "Movie session not found."}), 404

    if movie_id:
        movie_session.name = movie_id
    if auditorium_id:
        movie_session.description = auditorium_id
    if year:
        movie_session.date = movie_session.date.replace(year=year)
    if month:
        movie_session.date = movie_session.date.replace(month=month)
    if day:
        movie_session.date = movie_session.date.replace(day=day)
    if hour:
        movie_session.date = movie_session.date.replace(hour=hour)
    if minute:
        movie_session.date = movie_session.date.replace(minute=minute)

    movie_session.save_to_db()

    return jsonify({"message": "Updated"})


@movie_sessions_bp.route("/sessions/<int:id>", methods=["DELETE"])
def delete_movie_session(id):
    movie_session = MovieSessionsModel.delete_by_id(id)
    if movie_session == 404:
        return jsonify({"message": "Movie session not found."}), 404
    return jsonify({"message": "Deleted"})
