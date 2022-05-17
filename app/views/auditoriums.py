from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import AuditoriumModel
from constants import OFFSET_DEFAULT, LIMIT_DEFAULT
from app.decorators import admin_group_required

auditoriums_bp = Blueprint('auditorium', __name__)


@auditoriums_bp.route("/auditorium/", methods=["GET"])
def get_auditoriums():
    auditoriums = AuditoriumModel.return_all(OFFSET_DEFAULT, LIMIT_DEFAULT)

    return jsonify(auditoriums)


@auditoriums_bp.route("/auditorium/<int:id>", methods=["GET"])
def get_auditorium(id):
    auditorium = AuditoriumModel.find_by_id(id)
    if not auditorium:
        return jsonify({"message": "Auditorium not found."}), 404

    return jsonify(auditorium)


@auditoriums_bp.route("/auditorium", methods=["POST"])
@jwt_required()
@admin_group_required
def create_auditorium():
    if not request.json:
        return jsonify({"message": 'Please, specify "seats".'}), 400

    seats = request.json.get("seats")
    auditorium = AuditoriumModel(seats=seats)
    auditorium.save_to_db()

    return jsonify({"id": auditorium.id}), 201


@auditoriums_bp.route("/auditorium/<int:id>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def update_auditorium(id):
    seats = request.json.get("seats")

    auditorium = AuditoriumModel.find_by_id(id, to_dict=False)
    if not auditorium:
        return jsonify({"message": "Auditorium not found."}), 404

    if seats:
        auditorium.seats = seats

    auditorium.save_to_db()
    return jsonify({"message": "Updated"})


@auditoriums_bp.route("/auditorium/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_group_required
def delete_auditorium(id):
    auditorium = AuditoriumModel.delete_by_id(id)
    if auditorium == 404:
        return jsonify({"message": "Auditorium not found."}), 404
    return jsonify({"message": "Deleted"})
