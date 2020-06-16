from flask import (
	Blueprint,
	request,
	jsonify
)

from flask.views import MethodView

from database import db

from auth import auth_required

from services.transactions import TransactionsService

bp = Blueprint('transactions', __name__)

@bp.route('', methods=["POST"])
#@auth_required
def transactions():
	""" Обработка  """
	return f'Transactions POST - OK', 200

class TransactionIDView(MethodView):

	#@auth_required
	def get(self, transaction_id):
		""" Обработка  """
		return f'TransactionID:{transaction_id} GET - OK', 200
	
	#@auth_required
	def patch(self, transaction_id):
		""" Обработка  """
		return f'TransactionID:{transaction_id} PATCH - OK', 200
	
	#@auth_required
	def delete(self, transaction_id):
		""" Обработка  """
		return f'TransactionID:{transaction_id} DELETE - OK', 200

bp.add_url_rule(
	'/<int:transaction_id>',
	view_func=TransactionIDView.as_view('transaction_id')
)