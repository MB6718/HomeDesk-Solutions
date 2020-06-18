class TransactionsService:
	def __init__(self, connection):
		self.connection = connection
	
	def add_transaction(self, transaction):
		""" Добавление транзакции в БД """
		cur = self.connection.execute("""
			INSERT INTO transactions
				(date, type, amount, comment, category_id, account_id)
			VALUES (?, ?, ?, ?, ?, ?)
			""",
			(transaction['date'],
			 transaction['type'],
			 transaction['amount'],
			 transaction['comment'],
			 transaction['category_id'],
			 transaction['account_id'],
			)
		)
		self.connection.commit()
		transaction_id = cur.lastrowid
		
		cur = self.connection.execute("""
			SELECT *
			FROM transactions AS t
			WHERE t.id = ?
			""",
			(transaction_id,)
		)
		transaction = cur.fetchone()
		
		return dict(transaction)
	
	def get_transaction(self, transaction_id):
		""" Получение транзакции из БД """
		cur = self.connection.execute("""
			SELECT *
			FROM transactions AS t
			WHERE t.id = ?
			""",
			(transaction_id,)
		)
		transaction = cur.fetchone()
		
		return dict(transaction)
	
	def patch_transaction(self, transaction, transaction_id):
		""" Изменение транзакции в БД """
		if 'type' in transaction:
			cur = self.connection.execute("""
				UPDATE transactions
				SET type = ?
				WHERE transactions.id = ?
				""",
				(transaction['type'], transaction_id,)
			)
		if 'amount' in transaction:
			cur = self.connection.execute("""
				UPDATE transactions
				SET amount = ?
				WHERE transactions.id = ?
				""",
				(transaction['amount'], transaction_id,)
			)
		if 'comment' in transaction:
			cur = self.connection.execute("""
				UPDATE transactions
				SET comment = ?
				WHERE transactions.id = ?
				""",
				(transaction['comment'], transaction_id,)
			)
		if 'date' in transaction:
			cur = self.connection.execute("""
				UPDATE transactions
				SET date = ?
				WHERE transactions.id = ?
				""",
				(transaction['date'], transaction_id,)
			)
		if 'category_id' in transaction:
			cur = self.connection.execute("""
				UPDATE transactions
				SET category_id = ?
				WHERE transactions.id = ?
				""",
				(transaction['category_id'], transaction_id,)
			)
			
		self.connection.commit()
		
		cur = self.connection.execute("""
			SELECT *
			FROM transactions AS t
			WHERE t.id = ?
			""",
			(transaction_id,)
		)
		transaction = cur.fetchone()
		
		return dict(transaction)
	
	def del_transaction(self, transaction_id):
		""" Удаление транзакции из БД """
		cur = self.connection.execute("""
			DELETE FROM transactions
			WHERE transactions.id = ?
			""",
			(transaction_id,)
		)
		self.connection.commit()
