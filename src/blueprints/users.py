from flask import (
    Blueprint,
    request,
    jsonify,
)
import sqlite3
from marshmallow import ValidationError

from database import db
from exceptions import ConflictError
from validations import UsersSchema
from services.users import UsersService

bp = Blueprint('users', __name__)


@bp.route('', methods=['POST'])
def users():
    """ Обработка регистрации нового пользователя """
    try:
        user_data = UsersSchema().load(request.json)
    except ValidationError as error:
        return error.messages, 400
    else:
        with db.connection as con:
            service = UsersService(con)
            try:
                user = service.add_user(user_data)
            except ConflictError:
                return '', 409
        return jsonify(user), 201
