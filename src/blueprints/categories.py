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

from marshmallow import ValidationError
from validations import CreateCategorySchema

bp = Blueprint('categories', __name__)


class CategoriesView(MethodView):
    
    @auth_required
    def get(self, account_id):
        """Возвращает деревья категорий, принадлежащих пользователю"""
        with db.connection as con:
            service = CategoriesService(con)
            tree_categories = service.get_subcategories_tree(account_id)

        return jsonify(tree_categories), 200
    
    @auth_required
    def post(self, account_id):
        """Функция добавления категории"""
        try:
            category = CreateCategorySchema().load(request.json)
        except ValidationError as error:
            return jsonify(error.messages), 400
        else:
            with db.connection as con:
                service = CategoriesService(con)
                try:
                    category = service.create_category(category, account_id)
                except CategoryDoesNotExistError:
                    return '', 400
                except PermissionError:
                    return '', 403
                except CategoryConflictError as error:
                    return jsonify(dict(error.category)), 409
                return jsonify(category), 200

class CategoryIDView(MethodView):
    
    @auth_required
    @must_be_owner('category')
    def get(self, account_id, category_id):
        """Возвращает дерево категорий, начиная с category_id категории"""
        with db.connection as con:
            service = CategoriesService(con)
            tree_category = service.get_subcategories_tree(account_id, category_id)
            return jsonify(tree_category), 200
    
    @auth_required
    @must_be_owner('category')
    def patch(self, account_id, category_id):
        """Функция для весенний изменений в категорию"""
        with db.connection as con:
            service = CategoriesService(con)
            try:
                category = service.update_category(
                    dict(request.json),
                    category_id,
                    account_id
                )
            except CategoryDoesNotExistError:
                return '', 400
            except CategoryConflictError as error:
                return jsonify(dict(error.category)), 409
            except PermissionError:
                return '', 403
            else:
                return jsonify(category), 200
    
    @auth_required
    @must_be_owner('category')
    def delete(self, account_id, category_id):
        """Функция для удаления категории и всех её потомков"""
        with db.connection as con:
            service = CategoriesService(con)
            service.delete_category(category_id)
            return '', 204


bp.add_url_rule('', view_func=CategoriesView.as_view('categories'))
bp.add_url_rule(
    '/<int:category_id>',
    view_func=CategoryIDView.as_view('category_id')
)
