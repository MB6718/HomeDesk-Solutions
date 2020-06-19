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
		
		return self.get_transaction(cur.lastrowid)
	
	def get_transaction(self, transaction_id):
		""" Получение транзакции из БД """
		cur = self.connection.execute("""
			SELECT *
			FROM transactions AS t
			WHERE t.id = ?
			""",
			(transaction_id,)
		)
		
		return dict(cur.fetchone())
	
	def patch_transaction(self, transaction, transaction_id):
		""" Изменение транзакции в БД """
		for name, value in transaction.items():
			cur = self.connection.execute(f"""
				UPDATE transactions
				SET {name} = '{value}'
				WHERE transactions.id = ?
				""",
				(transaction_id,)
			)
		self.connection.commit()
		
		return self.get_transaction(transaction_id)
	
	def del_transaction(self, transaction_id):
		""" Удаление транзакции из БД """
		cur = self.connection.execute("""
			DELETE FROM transactions
			WHERE transactions.id = ?
			""",
			(transaction_id,)
		)
		self.connection.commit()
