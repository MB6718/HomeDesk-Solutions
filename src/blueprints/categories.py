from flask import (
	Blueprint,
	request,
	jsonify,
	session
)

from flask.views import MethodView

from database import db

from auth import (
	category_owner,
	auth_required
)

from services.categories import CategoriesService

bp = Blueprint('categories', __name__)

class CategoriesView(MethodView):

	@auth_required
	def get(self):
		""" Обработка  """
		user_id = session['account_id']
		with db.connection as con:
			cur = con.execute("""
			SELECT id, name
			FROM category
			WHERE account_id=? and parent_id is NULL  
			""",
				(user_id,)
			)
			parent_category = [dict(elem) for elem in cur.fetchall()]
			print(parent_category)
			if parent_category:
				for i in range(len(parent_category)):
					parent_category[i] = CategoriesService.subcategories(con, user_id, parent_category[i])
		return jsonify(parent_category), 200


	#@auth_required
	def post(self):
		""" Обработка  """
		return f'Categories POST - OK', 200

class CategoryIDView(MethodView):

	#@auth_required
	def get(self, category_id):
		""" Обработка  """
		return f'CategoryID:{category_id} GET - OK', 200

	@auth_required
	@category_owner
	def patch(self, category_id):
		""" Обработка  """
		return f'CategoryID:{category_id} PATCH - OK', 200

	@auth_required
	@category_owner
	def delete(self, category_id):
		""" Обработка  """
		return f'CategoryID:{category_id} DELETE - OK', 200


bp.add_url_rule('', view_func=CategoriesView.as_view('categories'))
bp.add_url_rule(
	'/<int:category_id>',
	view_func=CategoryIDView.as_view('category_id')
)
