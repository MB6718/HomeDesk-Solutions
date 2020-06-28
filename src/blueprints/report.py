from flask import (
    Blueprint,
    request,
    jsonify,
    session
)
from flask.views import MethodView

from database import db

from auth import auth_required
from services.report import ReportService

from exceptions import (
    PermissionError,
    CategoryDoesNotExistError,
)

bp = Blueprint('report', __name__)

class ReportView(MethodView):
    
    @auth_required
    def get(self, account_id):
        """ Обработка получения отчёта """
        query = dict(request.args)
        with db.connection as con:
            service = ReportService(con)
            try:
                response = service.get_report(account_id, dict_query=query)
            except PermissionError:
                return '', 403
            except CategoryDoesNotExistError:
                return '', 400
        return jsonify(response), 200


bp.add_url_rule('', view_func=ReportView.as_view('report'))
