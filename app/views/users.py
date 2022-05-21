from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from app.models import UserModel
from constants import OFFSET_DEFAULT, LIMIT_DEFAULT
from app.decorators import admin_group_required

users_bp = Blueprint('users', __name__)


@users_bp.route("/users/", methods=["GET"])
@jwt_required()
@admin_group_required
def get_users():
    """
    Get all users or by name as admin

    :return: json with users info
    """
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    email = request.args.get("email")
    offset = request.args.get("offset", OFFSET_DEFAULT)
    limit = request.args.get("limit", LIMIT_DEFAULT)
    if firstname and lastname:
        user = UserModel.find_by_name(firstname, lastname)
    elif email:
        user = UserModel.find_by_email(email)
    else:
        user = UserModel.return_all(offset, limit)
    return jsonify(user)


@users_bp.route("/users/inactive", methods=["GET"])
@jwt_required()
@admin_group_required
def get_inactive_users():
    """
    Get all inactive users as admin

    :return: json with users info
    """
    offset = request.args.get("offset", OFFSET_DEFAULT)
    limit = request.args.get("limit", LIMIT_DEFAULT)
    user = UserModel.return_all_inactive(offset, limit)
    return jsonify(user)


@users_bp.route("/users/<int:id>", methods=["GET"])
@jwt_required()
@admin_group_required
def get_user(id):
    """
    Get user info by id as admin

    :param id: id of user
    :return: json with user info
    """
    user = UserModel.find_by_id(id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    return jsonify(user)


@users_bp.route("/users", methods=["POST"])
@jwt_required()
@admin_group_required
def create_user():
    """
    Create user as admin

    :return: json with new user id
    """
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
        return {"message": f"Email {email} already used"}, 404

    user = UserModel(firstname=firstname, lastname=lastname, email=email,
                     hashed_password=UserModel.generate_hash(password), is_admin=is_admin, is_active=True)
    user.save_to_db()
    return jsonify({"id": user.id}), 201


@users_bp.route("/users/<int:id>", methods=["PATCH"])
@jwt_required()
def update_user(id):
    """
    Update user info by id as admin or only password as user

    :param id: id of user
    :return: json with message "Updated"
    """
    user = UserModel.find_by_id(id, to_dict=False)
    if not user:
        return jsonify({"message": "User not found."}), 404
    email = get_jwt().get("sub")
    current_user = UserModel.find_by_email(email, to_dict=False)
    groups = get_jwt().get("groups")
    errors = {}
    if "admin" in groups:
        firstname = request.json.get("firstname")
        lastname = request.json.get("lastname")
        email = request.json.get("email")
        password = request.json.get("password")
        is_admin = request.json.get("is_admin")
        is_active = request.json.get("is_active")

        if firstname:
            user.firstname = firstname
        if lastname:
            user.lastname = lastname
        if email:
            if not UserModel.find_by_email(email, to_dict=False):
                user.email = email
            else:
                errors = {"message": f"Updated, but email {email} already used"}

        if isinstance(is_admin, bool):
            user.is_admin = is_admin
        if isinstance(is_active, bool):
            user.is_active = is_active
        if password:
            user.hashed_password = UserModel.generate_hash(password)
        user.save_to_db()
    else:
        password = request.json.get("password")
        if current_user.id == user.id:
            if password:
                user.hashed_password = UserModel.generate_hash(password)
            user.save_to_db()
        else:
            return jsonify({"message": "Not allowed"}), 404
    if errors:
        assert jsonify(errors)
    else:
        return jsonify({"message": "Updated"})


@users_bp.route("/users/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    """
    Delete user by id

    :param id: id of user
    :return: json with message "Deleted"
    """
    user = UserModel.find_by_id(id)
    if not user:
        return jsonify({"message": "User not found."}), 404
    email = get_jwt().get("sub")
    current_user = UserModel.find_by_email(email, to_dict=False)
    groups = get_jwt().get("groups")
    if "admin" not in groups:
        if current_user.id != user["id"]:
            return jsonify({"message": "Not allowed"}), 405
    user = UserModel.delete_by_id(id)
    return jsonify({"message": "Deleted"})
