from flask import (
    Blueprint,
    request,
    session,
    jsonify
)

from database import db

from auth import auth_required

bp = Blueprint('report', __name__)


@bp.route('', methods=['GET'])
#@auth_required
def report():
    """ Обработка получения отчёта """
    select = 'SELECT * FROM transactions '
    select_sum = 'SELECT SUM(amount) FROM transactions '
    select_item_count = 'SELECT COUNT(id) FROM transactions '
    where = 'WHERE account_id = ? AND'
    params = list()
    
    params.append(session.get('account_id'))
    request_dict = dict(request.args)

    if 'from' in request_dict:
        where = f'date>=? AND'
        params.append(request_dict['from'])

    if 'to' in request_dict:
        where += f'date<=? AND'
        params.append(request_dict['to'])

    if 'type' in request_dict:
        where += f'type = ? AND'
        params.append(request_dict['type'])

    where = ' '.join(where.split()[:-1])
    if 'page_size' in request_dict:
        page_size = request_dict['page_size']
    else:
        page_size = 20

    if 'page' in request_dict:
        page = request_dict['page']
    else:
        page = 1

    with db.connection as con:
        cur = con.execute(select+where, tuple(params))
        transactions = [dict(elem) for elem in cur.fetchall()]

        cur = con.execute(select_sum+where,tuple(params))
        total = dict(cur.fetchone())['SUM(amount)']

        cur = con.execute(select_item_count+where, tuple(params))
        item_count = dict(cur.fetchone())['COUNT(id)']

        if item_count % page_size > 0:
            page_count = item_count//page_size + 1
        else:
            page_count = item_count//page_size

        response = dict()
        response['page_count'] = page_count
        response['page'] = page
        response['page_size'] = page_size
        response['item_count'] = item_count
        response['total'] = total
        response['transactions'] = transactions
    return jsonify(response), 200
