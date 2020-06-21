from datetime import datetime

from flask import (
	Blueprint,
	request,
	jsonify
)
from flask.views import MethodView

from auth import auth_required, transaction_owner
from database import db
from services.transactions import TransactionsService

bp = Blueprint('transactions', __name__)

class TransactionView(MethodView):
	
	@auth_required
	def post(self, user_id):
		""" Обработка добавления новой транзакции в БД """
		transaction = request.json
		type = transaction.get('type')
		amount = transaction.get('amount')
		date = transaction.get('date')
		category_id = transaction.get('category_id')
		comment = transaction.get('comment')
		
		if not type or not amount:
			return '', 400
		if not date:
			transaction['date'] = datetime.timestamp(datetime.now())
		if not category_id:
			transaction['category_id'] = 0
		if not comment:
			transaction['comment'] = ''
		
		transaction['account_id'] = user_id
		
		with db.connection as con:
			service = TransactionsService(con)
			transaction = service.add_transaction(transaction)
		return jsonify(transaction), 200

class TransactionIDView(MethodView):

	@auth_required
	@transaction_owner
	def get(self, transaction_id, user_id):
		""" Обработка получения транзакции из БД """
		with db.connection as con:
			service = TransactionsService(con)
			transaction = service.get_transaction(transaction_id)
		return jsonify(transaction), 200
	
	@auth_required
	@transaction_owner
	def patch(self, transaction_id, user_id):
		""" Обработка изменения  транзакции в БД """
		with db.connection as con:
			service = TransactionsService(con)
			transaction = service.patch_transaction(
				dict(request.json),
				transaction_id
			)
		return jsonify(transaction), 200
	
	@auth_required
	@transaction_owner
	def delete(self, transaction_id, user_id):
		""" Обработка удаления транзакции из БД """
		with db.connection as con:
			service = TransactionsService(con)
			service.del_transaction(transaction_id)
		return '', 204


bp.add_url_rule('',	view_func=TransactionView.as_view('transaction'))
bp.add_url_rule(
	'/<int:transaction_id>',
	view_func=TransactionIDView.as_view('transaction_id')
)