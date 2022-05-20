from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import GenresModel
from constants import OFFSET_DEFAULT, LIMIT_DEFAULT
from app.decorators import admin_group_required

genres_bp = Blueprint('genres', __name__)


@genres_bp.route("/genres/", methods=["GET"])
def get_genres():
    genre = request.args.get("genre")
    offset = request.args.get("offset", OFFSET_DEFAULT)
    limit = request.args.get("limit", LIMIT_DEFAULT)
    if genre:
        genre = GenresModel.find_by_genre(genre, without_sessions=True)
    else:
        genre = GenresModel.return_all(offset, limit, without_sessions=True)

    return jsonify(genre)


@genres_bp.route("/genres/<int:id>", methods=["GET"])
def get_genre(id):
    genre = GenresModel.find_by_id(id, without_sessions=True)
    if not genre:
        return jsonify({"message": "Genre not found."}), 404

    return jsonify(genre)


@genres_bp.route("/genres", methods=["POST"])
@jwt_required()
@admin_group_required
def create_genre():
    if not request.json:
        return jsonify({"message": 'Please, specify "genre".'}), 400
    genre = request.json.get("genre")
    genre = GenresModel(genre=genre)
    genre.save_to_db()
    return jsonify({"id": genre.id}), 201


@genres_bp.route("/genres/<int:id>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def update_genre(id):
    new_genre = request.json.get("genre")

    genre = GenresModel.find_by_id(id, to_dict=False)
    if not genre:
        return jsonify({"message": "Genre not found."}), 404

    if new_genre:
        genre.genre = new_genre
    genre.save_to_db()

    return jsonify({"message": "Updated"})


@genres_bp.route("/genres/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_group_required
def delete_genre(id):
    genre = GenresModel.delete_by_id(id)
    if genre == 404:
        return jsonify({"message": "Genre not found."}), 404
    return jsonify({"message": "Deleted"})
