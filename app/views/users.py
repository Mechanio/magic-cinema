from flask import jsonify, request, Blueprint
from app.models import UserModel
from constants import OFFSET_DEFAULT, LIMIT_DEFAULT

users_bp = Blueprint('users', __name__)


@users_bp.route("/users/", methods=["GET"])
def get_users():
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    email = request.args.get("email")
    if firstname and lastname:
        user = UserModel.find_by_name(firstname, lastname)
    elif email:
        user = UserModel.find_by_email(email)
    else:
        user = UserModel.return_all(OFFSET_DEFAULT, LIMIT_DEFAULT)
    return jsonify(user)


@users_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = UserModel.find_by_id(id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    return jsonify(user)


@users_bp.route("/users", methods=["POST"])
def create_user():
    if not request.json:
        return jsonify({"message": 'Please, specify "firstname", "lastname", "email", "password" and "is_admin".'}), 400

    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")
    email = request.json.get("email")
    password = request.json.get("password")
    is_admin = request.json.get("is_admin")

    if not firstname or not lastname or not email or not password or not isinstance(is_admin, bool):
        return jsonify({"message": 'Please, specify "firstname", "lastname", "email", "password" and "is_admin".'}), 400

    if UserModel.find_by_email(email, to_dict=False):
        return {"message": f"Email {email} already used"}

    user = UserModel(firstname=firstname, lastname=lastname, email=email,
                     hashed_password=UserModel.generate_hash(password), is_admin=is_admin, is_active=True)
    user.save_to_db()
    return jsonify({"id": user.id}), 201


@users_bp.route("/users/<int:id>", methods=["PATCH"])
def update_user(id):
    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")
    email = request.json.get("email")
    password = request.json.get("password")
    is_admin = request.json.get("is_admin")

    user = UserModel.find_by_id(id, to_dict=False)
    if not user:
        return jsonify({"message": "User not found."}), 404

    if firstname:
        user.firstname = firstname
    if lastname:
        user.lastname = lastname
    if email:
        user.firstname = email
    if isinstance(is_admin, bool):
        user.is_admin = is_admin
    if password:
        user.hashed_password = UserModel.generate_hash(password)
    user.save_to_db()
    return jsonify({"message": "Updated"})


@users_bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = UserModel.delete_by_id(id)
    if user == 404:
        return jsonify({"message": "User not found."}), 404
    return jsonify({"message": "Deleted"})
