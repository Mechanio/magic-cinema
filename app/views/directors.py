from flask import jsonify, request, Blueprint
from app.models import DirectorsModel
from constants import OFFSET_DEFAULT, LIMIT_DEFAULT

directors_bp = Blueprint('director', __name__)


@directors_bp.route("/director/", methods=["GET"])
def get_directors():
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    if firstname and lastname:
        director = DirectorsModel.find_by_name(firstname, lastname)
    else:
        director = DirectorsModel.return_all(OFFSET_DEFAULT, LIMIT_DEFAULT)
    return jsonify(director)


@directors_bp.route("/director/<int:id>", methods=["GET"])
def get_director(id):
    director = DirectorsModel.find_by_id(id)
    if not director:
        return jsonify({"message": "Director not found."}), 404

    return jsonify(director)


@directors_bp.route("/director", methods=["POST"])
def create_director():
    if not request.json:
        return jsonify({"message": 'Please, specify "firstname" and "lastname".'}), 400

    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")

    if not firstname or not lastname:
        return jsonify({"message": 'Please, specify "firstname" and "lastname".'}), 400
    director = DirectorsModel(firstname=firstname, lastname=lastname)
    director.save_to_db()
    return jsonify({"id": director.id}), 201


@directors_bp.route("/director/<int:id>", methods=["PATCH"])
def update_director(id):
    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")

    director = DirectorsModel.find_by_id(id, to_dict=False)
    if not director:
        return jsonify({"message": "Director not found."}), 404

    if firstname:
        director.firstname = firstname
    if lastname:
        director.lastname = lastname
    director.save_to_db()
    return jsonify({"message": "Updated"})


@directors_bp.route("/director/<int:id>", methods=["DELETE"])
def delete_director(id):
    director = DirectorsModel.delete_by_id(id)
    if director == 404:
        return jsonify({"message": "Director not found."}), 404
    return jsonify({"message": "Deleted"})
