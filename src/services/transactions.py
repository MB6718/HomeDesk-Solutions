from exceptions import (
    CategoryDoesNotExistError,
    PermissionError,
)
from services.categories import CategoriesService


class TransactionsService:
    def __init__(self, connection):
        self.connection = connection
    
    def category_check(self, category_id, account_id):
        if category_id is not None:
            CategoriesService.category_exists(self, category_id)
            CategoriesService.is_category_owner(self, category_id, account_id)
    
    def create_transaction(self, transaction, account_id):
        """ Добавление транзакции в БД """
        category_id = transaction['category_id']
        self.category_check(category_id, account_id)
        print(transaction)
        cur = self.connection.execute("""
            INSERT INTO transactions
                (date, type, amount, comment, category_id, account_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (transaction['date'],
             transaction['type'],
             transaction['amount'],
             transaction['comment'],
             category_id,
             account_id,
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
    
    def update_transaction(self, transaction, transaction_id, account_id):
        """ Изменение транзакции в БД """
        if 'category_id' in transaction:
            self.category_check(transaction['category_id'], account_id)
        fields = ', '.join(
            f'{name} = "{value}"' for name, value in transaction.items()
        )
        if 'category_id' in transaction and transaction['category_id'] is None:
            fields = fields.replace('"None"', 'NULL')
        cur = self.connection.execute(f"""
            UPDATE transactions
            SET {fields}
            WHERE transactions.id = ?
            """,
            (transaction_id,)
        )
        self.connection.commit()
        return self.get_transaction(transaction_id)
    
    def delete_transaction(self, transaction_id):
        """ Удаление транзакции из БД """
        cur = self.connection.execute("""
            DELETE FROM transactions
            WHERE transactions.id = ?
            """,
            (transaction_id,)
        )
        self.connection.commit()
