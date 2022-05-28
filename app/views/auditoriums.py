from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import AuditoriumModel
from constants import OFFSET_DEFAULT, LIMIT_DEFAULT
from app.decorators import admin_group_required

auditoriums_bp = Blueprint('auditorium', __name__)


@auditoriums_bp.route("/api/auditorium/", methods=["GET"])
def get_auditoriums():
    """
    Get all auditoriums

    :return: json with auditoriums info
    """
    offset = request.args.get("offset", OFFSET_DEFAULT)
    limit = request.args.get("limit", LIMIT_DEFAULT)
    auditoriums = AuditoriumModel.return_all(offset, limit)

    return jsonify(auditoriums)


@auditoriums_bp.route("/api/auditorium/<int:id_>", methods=["GET"])
def get_auditorium(id_):
    """
    Get auditorium info by id

    :param id_: id of auditorium
    :return: json with auditorium info
    """
    auditorium = AuditoriumModel.find_by_id(id_)
    if not auditorium:
        return jsonify({"message": "Auditorium not found."}), 404

    return jsonify(auditorium)


@auditoriums_bp.route("/api/auditorium/", methods=["POST"])
@jwt_required()
@admin_group_required
def create_auditorium():
    """
    Create auditorium as admin

    :return: json with new auditorium id
    """
    if not request.json:
        return jsonify({"message": 'Please, specify "seats".'}), 400

    seats = request.json.get("seats")
    auditorium = AuditoriumModel(seats=seats)
    auditorium.save_to_db()

    return jsonify({"id": auditorium.id}), 201


@auditoriums_bp.route("/api/auditorium/<int:id_>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def update_auditorium(id_):
    """
    Update auditorium info by id as admin

    :param id_: id of auditorium
    :return: json with message "Updated"
    """
    seats = request.json.get("seats")

    auditorium = AuditoriumModel.find_by_id(id_, to_dict=False)
    if not auditorium:
        return jsonify({"message": "Auditorium not found."}), 404

    if seats:
        auditorium.seats = seats

    auditorium.save_to_db()
    return jsonify({"message": "Updated"})


@auditoriums_bp.route("/api/auditorium/<int:id_>", methods=["DELETE"])
@jwt_required()
@admin_group_required
def delete_auditorium(id_):
    """
    Delete auditorium by id as admin

    :param id_: id of auditorium
    :return: json with message "Deleted"
    """
    auditorium = AuditoriumModel.delete_by_id(id_)
    if auditorium == 404:
        return jsonify({"message": "Auditorium not found."}), 404
    return jsonify({"message": "Deleted"})
