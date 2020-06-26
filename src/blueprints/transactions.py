from datetime import datetime, timezone
from flask import (
    Blueprint,
    request,
    jsonify,
)
from flask.views import MethodView
from marshmallow import ValidationError

from marshmallow import ValidationError

from auth import (
    must_be_owner,
    auth_required,
)
from database import db
from exceptions import (
    CategoryDoesNotExistError,
    PermissionError,
)
from services.transactions import TransactionsService

from services.validations import TransactionSchema

bp = Blueprint('transactions', __name__)

class TransactionView(MethodView):

    @auth_required
    def post(self, account_id):
        """ Обработка добавления новой транзакции в БД """
        try:
            transaction_data = TransactionSchema().load(request.json)
        except ValidationError as error:
            return jsonify(error.messages), 400
        else:
            if 'comment' not in transaction_data:
                transaction_data['comment'] = ''
            if 'date' not in transaction_data:
                transaction_data['date'] = datetime.now(tz=timezone.utc).timestamp()
            if 'category_id' not in transaction_data or \
                    transaction_data['category_id'] == 0:
                transaction_data['category_id'] = None
            with db.connection as con:
                service = TransactionsService(con)
                try:
                    transaction = service.create_transaction(
                        transaction_data,
                        account_id
                    )
                except CategoryDoesNotExistError:
                    return '', 404
                except PermissionError:
                    return '', 403
            return jsonify(transaction), 200

class TransactionIDView(MethodView):

    @auth_required
    @must_be_owner('transaction')
    def get(self, transaction_id, account_id):
        """ Обработка получения транзакции из БД """
        with db.connection as con:
            service = TransactionsService(con)
            transaction = service.get_transaction(transaction_id)
        return jsonify(transaction), 200

    @auth_required
    @must_be_owner('transaction')
    def patch(self, transaction_id, account_id):
        """ Обработка изменения транзакции в БД """
        try:
            transaction_data = TransactionSchema().load(request.json)
        except ValidationError as err:
            return err.messages, 400

        transaction = dict(transaction_data)
        transaction['account_id'] = account_id

        with db.connection as con:
            service = TransactionsService(con)
            try:
                transaction = service.update_transaction(
                    transaction,
                    transaction_id
                )
            except CategoryDoesNotExistError:
                return '', 404
            except PermissionError:
                return '', 403
        return jsonify(transaction), 200

    @auth_required
    @must_be_owner('transaction')
    def delete(self, transaction_id, account_id):
        """ Обработка удаления транзакции из БД """
        with db.connection as con:
            service = TransactionsService(con)
            service.delete_transaction(transaction_id)
        return '', 204


bp.add_url_rule('', view_func=TransactionView.as_view('transaction'))
bp.add_url_rule(
    '/<int:transaction_id>',
    view_func=TransactionIDView.as_view('transaction_id')
)
