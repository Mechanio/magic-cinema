from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import GenresModel
from constants import OFFSET_DEFAULT, LIMIT_DEFAULT
from app.decorators import admin_group_required

genres_bp = Blueprint('genres', __name__)


@genres_bp.route("/genres/", methods=["GET"])
def get_genres():
    """
    Get all genres or specific genre by name

    :return: json with genres info
    """
    genre = request.args.get("genre")
    offset = request.args.get("offset", OFFSET_DEFAULT)
    limit = request.args.get("limit", LIMIT_DEFAULT)
    if genre:
        genre = GenresModel.find_by_genre(genre, without_sessions=True)
    else:
        genre = GenresModel.return_all(offset, limit, without_sessions=True)

    return jsonify(genre)


@genres_bp.route("/genres/<int:id_>", methods=["GET"])
def get_genre(id_):
    """
    Get genre info by id

    :param id_: id of genre
    :return: json with genre info
    """
    genre = GenresModel.find_by_id(id_, without_sessions=True)
    if not genre:
        return jsonify({"message": "Genre not found."}), 404

    return jsonify(genre)


@genres_bp.route("/genres", methods=["POST"])
@jwt_required()
@admin_group_required
def create_genre():
    """
    Create genre as admin

    :return: json with new genre id
    """
    if not request.json:
        return jsonify({"message": 'Please, specify "genre".'}), 404
    genre = request.json.get("genre")
    genre = GenresModel(genre=genre)
    genre.save_to_db()
    return jsonify({"id": genre.id}), 201


@genres_bp.route("/genres/<int:id_>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def update_genre(id_):
    """
    Update genre info by id as admin

    :param id_: id of genre
    :return: json with message "Updated"
    """
    new_genre = request.json.get("genre")

    genre = GenresModel.find_by_id(id_, to_dict=False)
    if not genre:
        return jsonify({"message": "Genre not found."}), 404

    if new_genre:
        genre.genre = new_genre
    genre.save_to_db()

    return jsonify({"message": "Updated"})


@genres_bp.route("/genres/<int:id_>", methods=["DELETE"])
@jwt_required()
@admin_group_required
def delete_genre(id_):
    """
    Delete genre by id as admin

    :param id_: id of genre
    :return: json with message "Deleted"
    """
    genre = GenresModel.delete_by_id(id_)
    if genre == 404:
        return jsonify({"message": "Genre not found."}), 404
    return jsonify({"message": "Deleted"})
