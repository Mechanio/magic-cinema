from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import DirectorsModel
from constants import OFFSET_DEFAULT, LIMIT_DEFAULT
from app.decorators import admin_group_required


directors_bp = Blueprint('director', __name__)


@directors_bp.route("/api/director/", methods=["GET"])
def get_directors():
    """
    Get all directors or by name

    :return: json with directors info
    """
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    offset = request.args.get("offset", OFFSET_DEFAULT)
    limit = request.args.get("limit", LIMIT_DEFAULT)
    if firstname and lastname:
        director = DirectorsModel.find_by_name(firstname, lastname, without_sessions=True)
    else:
        director = DirectorsModel.return_all(offset, limit, without_sessions=True)
    return jsonify(director)


@directors_bp.route("/api/director/<int:id_>", methods=["GET"])
def get_director(id_):
    """
    Get director info by id

    :param id_: id of director
    :return: json with director info
    """
    director = DirectorsModel.find_by_id(id_, without_sessions=True)
    if not director:
        return jsonify({"message": "Director not found."}), 404

    return jsonify(director)


@directors_bp.route("/api/director/", methods=["POST"])
@jwt_required()
@admin_group_required
def create_director():
    """
    Create director as admin

    :return: json with new director id
    """
    if not request.json:
        return jsonify({"message": 'Please, specify "firstname" and "lastname".'}), 400

    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")

    if not firstname or not lastname:
        return jsonify({"message": 'Please, specify "firstname" and "lastname".'}), 400
    director = DirectorsModel(firstname=firstname, lastname=lastname)
    director.save_to_db()
    return jsonify({"id": director.id}), 201


@directors_bp.route("/api/director/<int:id_>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def update_director(id_):
    """
    Update director info by id as admin

    :param id_: id of director
    :return: json with message "Updated"
    """
    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")

    director = DirectorsModel.find_by_id(id_, to_dict=False)
    if not director:
        return jsonify({"message": "Director not found."}), 404

    if firstname:
        director.firstname = firstname
    if lastname:
        director.lastname = lastname
    director.save_to_db()
    return jsonify({"message": "Updated"}), 200


@directors_bp.route("/api/director/<int:id_>", methods=["DELETE"])
@jwt_required()
@admin_group_required
def delete_director(id_):
    """
    Delete director by id as admin

    :param id_: id of director
    :return: json with message "Deleted"
    """
    director = DirectorsModel.delete_by_id(id_)
    if director == 404:
        return jsonify({"message": "Director not found."}), 404
    return jsonify({"message": "Deleted"}), 200
