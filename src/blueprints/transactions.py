from datetime import datetime

from flask import (
	Blueprint,
	request,
	jsonify,
)
from flask.views import MethodView

from marshmallow import ValidationError

from auth import (
	must_be_owner,
	auth_required,
)
from database import db
from services.transactions import (
	TransactionsService,
	CategoryDoesNotExistError,
	CategoryDoesNotOwnerError,
)

from services.validations import TransactionSchema

bp = Blueprint('transactions', __name__)

class TransactionView(MethodView):
	
	@auth_required
	def post(self, account_id):
		""" Обработка добавления новой транзакции в БД """
		transaction = request.json

		try:
			transaction_data = TransactionSchema().load(transaction)
		except ValidationError as err:
			return err.messages, 400

		type = transaction_data.get('type')
		amount = transaction_data.get('amount')
		date = transaction_data.get('date')
		category_id = transaction_data.get('category_id')
		comment = transaction_data.get('comment')
		
		if not type or not amount:
			return '', 400
		if not date:
			transaction['date'] = datetime.timestamp(datetime.now())
		if not category_id:
			transaction['category_id'] = 0
		if not comment:
			transaction['comment'] = ''
		
		transaction['account_id'] = account_id
		
		with db.connection as con:
			service = TransactionsService(con)
			try:
				transaction = service.create_transaction(transaction)
			except CategoryDoesNotExistError:
				return '', 404
			except CategoryDoesNotOwnerError:
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
		transaction = dict(request.json)
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
			except CategoryDoesNotOwnerError:
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


bp.add_url_rule('',	view_func=TransactionView.as_view('transaction'))
bp.add_url_rule(
	'/<int:transaction_id>',
	view_func=TransactionIDView.as_view('transaction_id')
)
