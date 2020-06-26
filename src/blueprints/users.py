from marshmallow import ValidationError

from flask import (
    Blueprint,
    request,
    jsonify
)

from database import db

from services.validations import UsersSchema

from services.users import UsersService

bp = Blueprint('users', __name__)


@bp.route('', methods=['POST'])
def users():
    """ Обработка регистрации нового пользователя """
    request_json = request.json
    try:
        user_data = UsersSchema().load(request_json)
    except ValidationError as err:
        return err.messages, 400
    
    with db.connection as con:
        service = UsersService(con)
        user = service.get_user(request_json.get('email'))
        if user is not None:
            return "", 409
        user = service.add_user(user_data)
        return jsonify(dict(user)), 201
