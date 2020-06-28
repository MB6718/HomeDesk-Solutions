from exceptions import (
    CategoryDoesNotExistError,
    PermissionError,
)
from services.categories import CategoriesService


class TransactionsService:
    def __init__(self, connection):
        self.connection = connection
    
    def category_check(self, category_id, account_id):
        """ Проверяет существование и является ли account_id
            владельцем категории под category_id """
        if category_id is not None:
            CategoriesService(self.connection).parent_category_exists(category_id, account_id)
            CategoriesService(self.connection).is_category_owner(category_id, account_id)
    
    def create_transaction(self, transaction, account_id):
        """ Добавление транзакции в БД """
        category_id = transaction['category_id']
        self.category_check(category_id, account_id)
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
            FROM transactions
            WHERE id = ?
            """,
            (transaction_id,)
        )
        return dict(cur.fetchone())
    
    def update_transaction(self, transaction, transaction_id):
        """ редактирование транзакции в БД """
        fields = ', '.join(
            f'{name} = "{value}"' for name, value in transaction.items()
        )
        if 'category_id' in transaction:
            category_id = transaction['category_id']
            if category_id is None:
                fields = fields.replace('"None"', 'NULL')
            else:
                self.category_check(category_id, transaction['account_id'])
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
