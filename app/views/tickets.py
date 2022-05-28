from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt, jwt_required

from app.models import TicketsModel, MovieSessionsModel, UserModel
from constants import OFFSET_DEFAULT, LIMIT_DEFAULT
from app.decorators import admin_group_required


tickets_bp = Blueprint('tickets', __name__)


@tickets_bp.route("/api/tickets/", methods=["GET"])
@jwt_required()
def get_tickets():
    """
    Get current user tickets as user or all tickets as admin

    :return: json with actors info
    """
    email = get_jwt().get("sub")
    current_user = UserModel.find_by_email(email, to_dict=False)
    groups = get_jwt().get("groups")
    offset = request.args.get("offset", OFFSET_DEFAULT)
    limit = request.args.get("limit", LIMIT_DEFAULT)

    if "admin" in groups:
        session_id = request.args.get("session_id")
        user_id = request.args.get("user_id")
        if session_id:
            tickets = TicketsModel.find_by_session_id(session_id, offset, limit)
        elif user_id:
            tickets = TicketsModel.find_by_user_id(user_id, offset, limit)
        else:
            tickets = TicketsModel.return_all(offset, limit)
    else:
        tickets = TicketsModel.find_by_user_id(current_user.id, offset, limit)

    return jsonify(tickets)


@tickets_bp.route("/api/tickets/inactive", methods=["GET"])
@jwt_required()
def get_inactive_tickets():
    """
    Get current user inactive tickets as user or all inactive tickets as admin

    :return: json with actors info
    """
    email = get_jwt().get("sub")
    current_user = UserModel.find_by_email(email, to_dict=False)
    groups = get_jwt().get("groups")
    offset = request.args.get("offset", OFFSET_DEFAULT)
    limit = request.args.get("limit", LIMIT_DEFAULT)

    if "admin" in groups:
        session_id = request.args.get("session_id")
        user_id = request.args.get("user_id")
        if session_id:
            tickets = TicketsModel.find_by_session_id_inactive(session_id, offset, limit)
        elif user_id:
            tickets = TicketsModel.find_by_user_id_inactive(user_id, offset, limit)
        else:
            tickets = TicketsModel.return_all_inactive(offset, limit)
    else:
        tickets = TicketsModel.find_by_user_id_inactive(current_user.id, offset, limit)

    return jsonify(tickets)


@tickets_bp.route("/api/tickets/<int:id_>", methods=["GET"])
@jwt_required()
def get_ticket(id_):
    """
    Get ticket info by id

    :param id_: id of ticket
    :return: json with ticket info
    """
    email = get_jwt().get("sub")
    current_user = UserModel.find_by_email(email, to_dict=False)
    ticket = TicketsModel.find_by_id(id_)
    if not ticket:
        return jsonify({"message": "Ticket not found."}), 404

    groups = get_jwt().get("groups")
    if "admin" not in groups:
        if current_user.id != ticket["user_id"]:
            return jsonify({"message": "Not allowed"}), 405

    return jsonify(ticket)


@tickets_bp.route("/api/tickets/", methods=["POST"])
@jwt_required()
def create_ticket():
    """
    Create ticket as user

    :return: json with new ticket id
    """
    email = get_jwt().get("sub")
    current_user = UserModel.find_by_email(email, to_dict=False)
    groups = get_jwt().get("groups")
    if "admin" in groups:
        if not request.json:
            return jsonify({"message": 'Please, specify "session_id", "user_id"'}), 400

        session_id = request.json.get("session_id")
        user_id = request.json.get("user_id")

        if not user_id:
            user_id = current_user.id
        if not session_id or not user_id:
            return jsonify({"message": 'Please, specify session_id, user_id.'}), 400

        current_session = MovieSessionsModel.find_by_id(session_id, to_dict=False)
        if current_session.remain_seats == 0:
            return jsonify({"message": "No more seats available"})
        current_session.remain_seats -= 1
        current_session.save_to_db()

        ticket = TicketsModel(session_id=session_id, user_id=user_id, is_active=True)
        ticket.save_to_db()
    else:
        session_id = request.json.get("session_id")
        if not session_id:
            return jsonify({"message": 'Please, specify session_id.'}), 400

        current_session = MovieSessionsModel.find_by_id(session_id, to_dict=False)
        if current_session.remain_seats == 0:
            return jsonify({"message": "No more seats available"}), 405
        current_session.remain_seats -= 1
        current_session.save_to_db()

        ticket = TicketsModel(session_id=session_id, user_id=current_user.id, is_active=True)
        ticket.save_to_db()

    return jsonify({"id": ticket.id}), 201


@tickets_bp.route("/api/tickets/<int:id_>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def update_ticket(id_):
    """
    Update ticket info by id as admin

    :param id_: id of ticket
    :return: json with message "Updated"
    """
    session_id = request.json.get("session_id")
    user_id = request.json.get("user_id")
    is_active = request.json.get("is_active")

    ticket = TicketsModel.find_by_id(id_, to_dict=False)
    if not ticket:
        return jsonify({"message": "Ticket not found."}), 404

    if session_id:
        current_session = MovieSessionsModel.find_by_id(ticket.session_id, to_dict=False)
        current_session.remain_seats += 1
        current_session.save_to_db()
        ticket.session_id = session_id
        new_current_session = MovieSessionsModel.find_by_id(session_id, to_dict=False)
        if new_current_session.remain_seats == 0:
            return jsonify({"message": "No more seats available"}), 405
        new_current_session.remain_seats -= 1
        new_current_session.save_to_db()
    if user_id:
        ticket.user_id = user_id
    if isinstance(is_active, bool):
        ticket.is_active = is_active

    ticket.save_to_db()

    return jsonify({"message": "Updated"})


@tickets_bp.route("/api/tickets/<int:id_>", methods=["DELETE"])
@jwt_required()
def delete_ticket(id_):
    """
    Delete ticket by id as user

    :param id_: id of ticket
    :return: json with message "Deleted"
    """
    ticket = TicketsModel.find_by_id(id_, to_dict=False)
    if not ticket:
        return jsonify({"message": "Ticket not found."}), 404
    email = get_jwt().get("sub")
    current_user = UserModel.find_by_email(email, to_dict=False)
    groups = get_jwt().get("groups")
    if "admin" not in groups:
        if current_user.id != ticket["user_id"]:
            return jsonify({"message": "Not allowed"}), 405

    current_session = MovieSessionsModel.find_by_id(ticket.session_id, to_dict=False)
    current_session.remain_seats += 1
    current_session.save_to_db()
    ticket = TicketsModel.delete_by_id(id_)
    return jsonify({"message": "Deleted"})
