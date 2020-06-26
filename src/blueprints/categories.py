from flask import (
    Blueprint,
    request,
    jsonify,
)
from flask.views import MethodView

from auth import (
    must_be_owner,
    auth_required,
)
from database import db
from services.categories import CategoriesService
from exceptions import (
    PermissionError,
    CategoryConflictError,
    CategoryDoesNotExistError,
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
                FROM categories
                WHERE account_id = ? and parent_id is NULL
                """,
                (account_id,)
            )
            parent_category = [dict(elem) for elem in cur.fetchall()]
            if parent_category:
                for i in range(len(parent_category)):
                    parent_category[i] = service.get_subcategories_tree(
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
                category = service.create_category(category, account_id)
            except CategoryDoesNotExistError:
                return '', 400
            except PermissionError:
                return '', 403
            except CategoryConflictError as e:
                return jsonify(dict(e.category)), 409
            else:
                return jsonify(category), 200

class CategoryIDView(MethodView):
    
    @auth_required
    @must_be_owner('category')
    def get(self, account_id, category_id):
        """Возвращает дерево категорий, начиная с category_id категории"""
        with db.connection as con:
            cur = con.execute("""
                SELECT id, name
                FROM categories
                WHERE account_id = ? and id = ?
                """,
                (account_id, category_id,)
            )
            parent_category = cur.fetchone()
            service = CategoriesService(con)

            tree_category = service.get_subcategories_tree(
                con,
                account_id,
                dict(parent_category)
            )
            return jsonify(tree_category), 200
    
    @auth_required
    @must_be_owner('category')
    def patch(self, account_id, category_id):
        """Функция для внесений изменений в категорию"""
        request_json = request.json
        with db.connection as con:
            service = CategoriesService(con)
            try:
                category = service.update_category(request_json, category_id, account_id)
            except CategoryDoesNotExistError:
                return '', 400
            except CategoryConflictError as e:
                return jsonify(dict(e.category)), 409
            except PermissionError:
                return '', 403
            else:
                return jsonify(category), 200
    
    @auth_required
    @must_be_owner('category')
    def delete(self, account_id, category_id):
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
