from flask import (
	Blueprint,
	request,
	jsonify
)

from flask.views import MethodView

from database import db

from auth import auth_required

from services.categories import (
	CategoriesService,
	CategoryDoesNotExistError,
	CategoryExistError,
)

bp = Blueprint('categories', __name__)

class CategoriesView(MethodView):

	#@auth_required
	def get(self):
		""" Обработка  """
		return f'Categories GET - OK', 200
	
	@auth_required
	def post(self, account_id):
		request_json = request.json
		with db.connection as con:
			service = CategoriesService(con)
			try:
				category = service.add_category(request_json, account_id)
			except CategoryDoesNotExistError:
				return '', 404
			except CategoryExistError as e:
				return jsonify(dict(e.category)), 409
			else:
				return jsonify(category), 200

class CategoryIDView(MethodView):

	#@auth_required
	def get(self, category_id):
		""" Обработка  """
		return f'CategoryID:{category_id} GET - OK', 200
	
	@auth_required
	def patch(self, category_id):
		request_json = request.json
		with db.connection as con:
			service = CategoriesService(con)
			try:
				category = service.patch_category(request_json, category_id)
			except CategoryDoesNotExistError:
				return '', 404
			else:
				return jsonify(category), 201
	
	@auth_required
	def delete(self, category_id):
		with db.connection as con:
			service = CategoriesService(con)
			service.delete_category(category_id)
			return '', 204


bp.add_url_rule('', view_func=CategoriesView.as_view('categories'))
bp.add_url_rule(
	'/<int:category_id>',
	view_func=CategoryIDView.as_view('category_id')
)
