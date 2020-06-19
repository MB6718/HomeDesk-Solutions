import sqlite3

from exceptions import ServiceError


class CategoriesServiceError(ServiceError):
    service = 'categories'


class CategoryDoesNotExistError(CategoriesServiceError):
    pass

class CategoryExistError(CategoriesServiceError):
	def __init__(self, category):
		self.category = category


class CategoriesService:
	def __init__(self, connection):
		self.connection = connection
		
	def check_parent_id(self, parent_id):
		cur = self.connection.cursor()
		cur.execute(
			'SELECT c.name, c.id '
			'FROM category AS c '
			'WHERE c.id = ?',
			(parent_id,)
		)
		parent_category = cur.fetchone()
		if parent_category is None:
			raise CategoryDoesNotExistError
		return parent_category
	
	def add_category(self, request_json, account_id):
		""" Создание категории в БД """
		cur = self.connection.cursor()
		name_category = request_json.get('name').lower()
		parent_id = request_json.get('parent_id')
		query = (
			'SELECT c.name, c.id '
			'FROM category AS c '
			'WHERE c.name = ? AND account_id = ?'
		)
		cur.execute(query, (name_category, account_id,))
		category = cur.fetchone()
		
		if category is not None:
			raise CategoryExistError(category)
		
		if parent_id:
			parent_category = self.check_parent_id(parent_id)

		cur.execute(
			'INSERT INTO category (account_id, parent_id, name) '
			'VALUES (?, ?, ?) ',
			(account_id, parent_id, name_category)
		)

		cur.execute(query, (name_category, account_id,))
		result = dict(cur.fetchone())
		if parent_id:
			parent_category = dict(parent_category)
			parent_category['subcategory'] = result
			result = parent_category
			
		self.connection.commit()
		return result

	
	def delete_category(self, category_id):
		""" Удаление категории из БД. При удаление категории родителя удаляются все наследующиеся от него категории-дети"""
		cur = self.connection.cursor()
		list_id = []
		list_id.append(category_id)
		for id in list_id:
			cur.execute(f"""
				SELECT id
				FROM category
				WHERE parent_id = {id}
				""")
			result = cur.fetchall()
			if result:
				for elem in result:
					list_id.append(elem[0])

			cur.execute(f"""
				DELETE FROM category
				WHERE id = {id}
				""")
		self.connection.commit()
		
	
	def patch_category(self, request_json, category_id):
		cur = self.connection.cursor()
		parent_id = request_json.get('parent_id')
		if parent_id:
			parent_category = self.check_parent_id(parent_id)
		for key, value in request_json.items():
			if key == 'name':
				value = value.lower()
			cur.execute(f"""
		        UPDATE category
		        SET {key} = '{value}'
		        WHERE id= {category_id}
		    """)
		query = (
			'SELECT c.name, c.id '
			'FROM category AS c '
			'WHERE id = ? '
		)
		cur.execute(query, (category_id,))
		result = dict(cur.fetchone())
		if parent_id:
			parent_category = dict(parent_category)
			parent_category['subcategory'] = result
			result = parent_category
		
		self.connection.commit()
		return result