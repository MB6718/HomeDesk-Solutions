from flask import (
	Blueprint,
	request,
	jsonify
)

from flask.views import MethodView

from database import db

from auth import auth_required

from services.categories import CategoriesService

bp = Blueprint('categories', __name__)

class CategoriesView(MethodView):

	#@auth_required
	def get(self):
		""" Обработка  """
		return f'Categories GET - OK', 200
	
	#@auth_required
	def post(self):
		""" Обработка  """
		return f'Categories POST - OK', 200

class CategoryIDView(MethodView):

	#@auth_required
	def get(self, category_id):
		""" Обработка  """
		return f'CategoryID:{category_id} GET - OK', 200
	
	#@auth_required
	def patch(self, category_id):
		""" Обработка  """
		return f'CategoryID:{category_id} PATCH - OK', 200
	
	#@auth_required
	def delete(self, category_id):
		""" Обработка  """
		return f'CategoryID:{category_id} DELETE - OK', 200

bp.add_url_rule('', view_func=CategoriesView.as_view('categories'))
bp.add_url_rule(
	'/<int:category_id>',
	view_func=CategoryIDView.as_view('category_id')
)
