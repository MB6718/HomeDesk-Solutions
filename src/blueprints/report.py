from flask import (
    Blueprint,
    request,
    session
)

from database import db

bp = Blueprint('report', __name__)

@bp.route('')
#@auth_required
def report():
    """ Обработка получения отчёта """
    return 'Report GET - OK', 200