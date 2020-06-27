from exceptions import (
    PermissionError,
    CategoryConflictError,
    CategoryDoesNotExistError,
)

class CategoriesService:
    def __init__(self, connection):
        self.connection = connection
    
    @staticmethod
    def get_subcategories_tree(con, account_id, parent_category):
        """Получение дерева категорий"""
        cur = con.execute("""
            SELECT id, name
            FROM categories
            WHERE account_id=? and parent_id = ?
            """,
            (account_id, parent_category['id'])
        )
        subcategory = [dict(elem) for elem in cur.fetchall()]
        if subcategory:
            for i in range(len(subcategory)):
                subcategory[i] = CategoriesService.get_subcategories_tree(
                    con,
                    account_id,
                    subcategory[i]
                )
        parent_category['subcategory'] = subcategory
        return parent_category
    
    def parent_category_exists(self, parent_id, account_id, category_id=None):
        """Проверка существования родительской категории"""
        parent_category = self.get_category(parent_id)
        if parent_id == category_id:
            raise CategoryConflictError(parent_category)
        if parent_category is None:
            raise CategoryDoesNotExistError
        if parent_category['account_id'] != account_id:
            raise PermissionError
        parent_category = dict(parent_category)
        parent_category.pop('account_id')
        return parent_category
    
    def get_category(self, category_id):
        """Получение категории по id"""
        cur = self.connection.execute("""
            SELECT id, name, account_id
            FROM categories
            WHERE id = ?
            """,
            (category_id,)
        )
        return cur.fetchone()
    
    def is_category_owner(self, category_id, account_id):
        """Проверка хозяина категории (для родительской)"""
        category = dict(self.get_category(category_id))
        if category['account_id'] != account_id:
            raise PermissionError
    
    def category_exists(self, category_id):
        """Проверка существования категории (для родительской)"""
        category = self.get_category(category_id)
        if category is None:
            raise CategoryDoesNotExistError
    
    def category_check(self, account_id, name_category):
        """Проверка категории на существование по имени"""
        cur = self.connection.cursor()
        query = ("""
            SELECT c.name, c.id
            FROM categories AS c
            WHERE c.name = ? AND account_id = ?
            """
        )
        cur.execute(query, (name_category, account_id,))
        category = cur.fetchone()
        
        if category is not None:
            raise CategoryConflictError(category)
        return query
    
    def create_category(self, category, account_id):
        """ Создание категории в БД """
        cur = self.connection.cursor()
        name_category = category.get('name')
        parent_id = category.get('parent_id')
        query = self.category_check(account_id, name_category)
        if parent_id:
            parent_category = self.parent_category_exists(parent_id, account_id)
        
        cur.execute("""
            INSERT INTO categories (account_id, parent_id, name)
            VALUES (?, ?, ?)
            """,
            (account_id, parent_id, name_category)
        )
        self.connection.commit()
        
        cur.execute(query, (name_category, account_id,))
        result = dict(cur.fetchone())
        if parent_id:
            parent_category = dict(parent_category)
            parent_category['subcategory'] = result
            result = parent_category
        
        return result
    
    def delete_category(self, category_id):
        """ Удаление категории из БД. При удаление категории родителя удаляются
            все наследующиеся от него категории-дети """
        cur = self.connection.cursor()
        list_id = []
        list_id.append(category_id)
        for id in list_id:
            cur.execute(f"""
                SELECT id
                FROM categories
                WHERE parent_id = {id}
                """
            )
            result = cur.fetchall()
            if result:
                for elem in result:
                    list_id.append(elem[0])
            
            cur.execute(f"""
                DELETE FROM categories
                WHERE id = {id}
                """
            )
        self.connection.commit()
    
    def update_category(self, request_json, category_id, account_id):
        fields = ', '.join(
            f'{name} = "{value}"' for name, value in request_json.items()
        )
        if 'name' in request_json:
            self.category_check(account_id, request_json['name'])
        if 'parent_id' in request_json:
            parent_category = dict(self.parent_category_exists(
                request_json['parent_id'],
                account_id,
                category_id=category_id
            ))
        self.connection.execute(f"""
            UPDATE categories
            SET {fields}
            WHERE id = ?
            """,
            (category_id,)
        )
        self.connection.commit()
        category = dict(self.get_category(category_id))
        category.pop('account_id')
        if 'parent_id' in request_json:
            parent_category['subcategory'] = category
            return parent_category
        else:
            return category
        