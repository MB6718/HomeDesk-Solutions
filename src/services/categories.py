import sqlite3

from exceptions import ServiceError


class CategoriesServiceError(ServiceError):
    service = 'categories'


class CategoryDoesNotExistError(CategoriesServiceError):
    pass


class NotEnoughRightsError(CategoriesServiceError):
	pass


class CategoryExistError(CategoriesServiceError):
	def __init__(self, category):
		self.category = category


class CategoriesService:
	def __init__(self, connection):
		self.connection = connection
	
	@staticmethod
	def get_subcategories_tree(con, account_id, parent_category):
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

	

	def parent_category_exists(self, parent_id, account_id):
		cur = self.connection.cursor()
		cur.execute(
			'SELECT c.name, c.id '
			'FROM categories AS c '
			'WHERE c.id = ?',
			(parent_id,)
		)
		parent_category = cur.fetchone()
		if parent_category is None:
			raise CategoryDoesNotExistError
		cur.execute(f"""
			SELECT c.account_id
			FROM categories AS c
			WHERE c.id = ?
			""",
			(parent_id,)
		)
		result = cur.fetchone()
		if result['account_id'] != account_id:
			raise NotEnoughRightsError
		return parent_category


	def category_exists(self, account_id, name_category):
		cur = self.connection.cursor()
		query = (
			'SELECT c.name, c.id '
			'FROM categories AS c '
			'WHERE c.name = ? AND account_id = ?'
		)
		cur.execute(query, (name_category, account_id,))
		category = cur.fetchone()
		
		if category is not None:
			raise CategoryExistError(category)
		return query


	def create_category(self, category, account_id):
		""" Создание категории в БД """
		cur = self.connection.cursor()
		name_category = category.get('name').lower()
		parent_id = category.get('parent_id')
		query = self.category_exists(account_id, name_category)
		if parent_id:
			parent_category = self.parent_category_exists(parent_id, account_id)

		cur.execute(
			'INSERT INTO categories (account_id, parent_id, name) '
			'VALUES (?, ?, ?) ',
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
		""" Удаление категории из БД. При удаление категории родителя удаляются все наследующиеся от него категории-дети"""
		cur = self.connection.cursor()
		list_id = []
		list_id.append(category_id)
		for id in list_id:
			cur.execute(f"""
				SELECT id
				FROM categories
				WHERE parent_id = {id}
				""")
			result = cur.fetchall()
			if result:
				for elem in result:
					list_id.append(elem[0])

			cur.execute(f"""
				DELETE FROM categories
				WHERE id = {id}
				""")
		self.connection.commit()

		

	def update_category(self, request_json, category_id, account_id):
		cur = self.connection.cursor()
		parent_id = request_json.get('parent_id')
		if parent_id:
			if parent_id != 'NULL':
				parent_category = self.parent_category_exists(parent_id, account_id)
		for key, value in request_json.items():
			if key == 'name':
				value = value.lower()
				self.category_exists(account_id, value)
			cur.execute(f"""
				UPDATE categories
				SET {key} = '{value}'
				WHERE id= {category_id}
			""")

		query = (
			'SELECT c.name, c.id '
			'FROM categories AS c '
			'WHERE id = ? '
		)
		cur.execute(query, (category_id,))
		result = dict(cur.fetchone())
		if parent_id and parent_id != 'NULL':
			parent_category = dict(parent_category)
			parent_category['subcategory'] = result
			result = parent_category
		
		self.connection.commit()
		return result
