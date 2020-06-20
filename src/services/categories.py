class CategoriesService:
	def __init__(self, connection):
		self.connection = connection
	
	def stub(self):
		pass

	@staticmethod
	def subcategories(con, user_id, pc):
		cur = con.execute("""
			SELECT id, name
			FROM category
			WHERE account_id=? and parent_id = ?  
			""",
				(user_id, pc['id'])
			)
		subcategory = [dict(elem) for elem in cur.fetchall()]
		if subcategory:
			for i in range(len(subcategory)):
				subcategory[i] = CategoriesService.subcategories(con, user_id, subcategory[i])
		pc['subcategory'] = subcategory
		return pc
