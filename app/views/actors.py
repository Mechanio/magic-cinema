from flask import jsonify, request, Blueprint

from app.models import ActorsModel
from constants import OFFSET_DEFAULT, LIMIT_DEFAULT

actors_bp = Blueprint('actors', __name__)


@actors_bp.route("/actors/", methods=["GET"])
def get_actors():
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    if firstname and lastname:
        actor = ActorsModel.find_by_name(firstname, lastname)
    else:
        actor = ActorsModel.return_all(OFFSET_DEFAULT, LIMIT_DEFAULT)
    return jsonify(actor)


@actors_bp.route("/actors/<int:id>", methods=["GET"])
def get_actor(id):
    actor = ActorsModel.find_by_id(id)
    if not actor:
        return jsonify({"message": "Actor not found."}), 404

    return jsonify(actor)


@actors_bp.route("/actors", methods=["POST"])
def create_actor():
    if not request.json:
        return jsonify({"message": 'Please, specify "firstname", and "lastname".'}), 400

    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")

    if not firstname or not lastname:
        return jsonify({"message": 'Please, specify "firstname", and "lastname".'}), 400
    actor = ActorsModel(firstname=firstname, lastname=lastname)
    actor.save_to_db()
    return jsonify({"id": actor.id}), 201


@actors_bp.route("/actors/<int:id>", methods=["PATCH"])
def update_actor(id):
    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")

    actor = ActorsModel.find_by_id(id, to_dict=False)
    if not actor:
        return jsonify({"message": "Actor not found."}), 404

    if firstname:
        actor.firstname = firstname
    if lastname:
        actor.lastname = lastname
    actor.save_to_db()
    return jsonify({"message": "Updated"})


@actors_bp.route("/actors/<int:id>", methods=["DELETE"])
def delete_actor(id):
    actor = ActorsModel.delete_by_id(id)
    if actor == 404:
        return jsonify({"message": "Actor not found."}), 404
    return jsonify({"message": "Deleted"})