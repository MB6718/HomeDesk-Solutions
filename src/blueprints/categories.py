from flask import (
	Blueprint,
	request,
	jsonify
)

from flask.views import MethodView

from database import db

from auth import (
	category_owner,
	auth_required
)

from services.categories import (
	CategoriesService,
	CategoryDoesNotExistError,
	CategoryExistError,
)

bp = Blueprint('categories', __name__)

class CategoriesView(MethodView):

	@auth_required
	def get(self, account_id):
		"""Возвращает деревья категорий, принадлежащих пользотелю"""
		with db.connection as con:
			service = CategoriesService(con)
			cur = con.execute("""
				SELECT id, name
				FROM category
				WHERE account_id = ? and parent_id is NULL
				""",
				(account_id,)
			)
			parent_category = [dict(elem) for elem in cur.fetchall()]
			if parent_category:
				for i in range(len(parent_category)):
					parent_category[i] = service.get_tree_subcategories(
						con,
						account_id,
						parent_category[i]
					)
		return jsonify(parent_category), 200
	
	@auth_required
	def post(self, account_id):
		"""Функция добавления категории"""
		category = request.json
		name = category.get('name')
		parent_id = category.get('parent_id')
		if not name:
			return '', 400
		with db.connection as con:
			service = CategoriesService(con)
			try:
				category = service.add_category(category, account_id)
			except CategoryDoesNotExistError:
				return '', 404
			except CategoryExistError as e:
				return jsonify(dict(e.category)), 409
			else:
				return jsonify(category), 200

class CategoryIDView(MethodView):
	@auth_required
	@category_owner
	def get(self, account_id, category_id):
		"""Возвращает дерево категорий, начиная с category_id категории"""
		with db.connection as con:
			cur = con.execute("""
				SELECT id, name
				FROM category
				WHERE account_id = ? and id = ?
				""",
				(account_id, category_id,)
			)
			parent_category = cur.fetchone()
			service = CategoriesService(con)
			tree_category = service.get_tree_subcategories(
				con,
				account_id,
				dict(parent_category)
			)
			return jsonify(tree_category), 201
	
	@auth_required
	@category_owner
	def patch(self, category_id, account_id):
		"""Функция для внесений изменений в категорию"""
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
	@category_owner
	def delete(self, category_id, account_id):
		"""Функция для удаления категории и всех ёё потомков"""
		with db.connection as con:
			service = CategoriesService(con)
			service.delete_category(category_id)
			return '', 204



bp.add_url_rule('', view_func=CategoriesView.as_view('categories'))
bp.add_url_rule(
	'/<int:category_id>',
	view_func=CategoryIDView.as_view('category_id')
)
