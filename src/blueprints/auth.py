from flask import (
    Blueprint,
    request,
    session,
    jsonify,
)
from marshmallow import ValidationError

from database import db
from exceptions import PermissionError
from validations import AuthSchema
from services.auth import AuthService

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login():
    """ Обработка аутентификации пользователя """
    try:
        auth_data = AuthSchema().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400
    else:
        with db.connection as con:
            service = AuthService(con)
            try:
                session['account_id'] = service.login_user(auth_data)
            except PermissionError:
                return '', 403
        return '', 200

@bp.route('/logout', methods=['POST'])
def logout():
    """Обработка выхода(деаутентификации) пользователя"""
    session.pop('account_id', None)
    return '', 200
