import sqlite3


class CategoriesService:
	def __init__(self, connection):
		self.connection = connection
	
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
			return dict(category), 409
		
		if parent_id:
			cur.execute(
				'SELECT c.name, c.id '
				'FROM category AS c '
				'WHERE c.id = ?',
				(parent_id,)
			)
			parent_category = cur.fetchone()
			
			if parent_id and parent_category == None:
				return '', 404

		cur.execute(
			'INSERT INTO category (account_id, parent_id, name) '
			'VALUES (?, ?, ?) ',
			(account_id, parent_id, name_category)
		)

		cur.execute(query, (name_category, account_id,))
		result = dict(cur.fetchone())
		if parent_id:
			result['subcategory'] = dict(parent_category)
			
		self.connection.commit()
		return result, 200

	
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
			print(result)
			if result:
				for elem in result:
					list_id.append(elem[0])

			cur.execute(f"""
				DELETE FROM category
				WHERE id = {id}
				""")
		self.connection.commit()
		return
