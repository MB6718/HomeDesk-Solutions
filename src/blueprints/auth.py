from flask import (
    Blueprint,
    request,
    session,
)
from werkzeug.security import check_password_hash

from database import db


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login():
    request_json = request.json
    email = request_json.get('email')
    password = request_json.get('password')

    if not email or not password:
        return '', 400

    with db.connection as con:
        cur = con.execute(
            'SELECT * '
            'FROM account '
            'WHERE email = ?',
            (email,),
        )
        user = cur.fetchone()

    if user is None:
        return '', 404

    if not check_password_hash(user['password'], password):
        return '', 403

    session['account_id'] = user['id']
    return 'login - OK', 200


@bp.route('/logout', methods=['POST'])
def logout():
    session.pop('account_id', None)
    return 'logout - OK', 200
