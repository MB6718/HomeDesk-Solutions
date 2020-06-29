from services.categories import CategoriesService


class ReportService:
    
    def __init__(self, connection):
        self.connection = connection
    
    def build_report_query(self, filters):
        """Конструктор запроса WHERE"""
        query_template = """
            {where_query}
            ORDER BY date
            """
        where_clauses = []
        params = []
        for key, value in filters.items():
            if key == 'category_id':
                """Проверка категории на существование, наличие прав"""
                if value == '0':
                    where_clauses.append(f' {key} is NULL ')
                else:
                    CategoriesService(self.connection).parent_category_exists(value, filters['account_id'])
                    """Поиск всех категорий-детей"""
                    cur = self.connection.execute(f"""
                        WITH RECURSIVE subtree(id)
                        AS (SELECT id
                            FROM categories
                            WHERE account_id = {filters['account_id']} AND id = {value}
                        UNION ALL
                            SELECT categories.id
                            FROM categories
                            INNER JOIN subtree ON categories.parent_id = subtree.id)
                        SELECT id
                        FROM subtree
                        ORDER BY id
                        """,
                    )
                    list_id = []
                    for elem in cur.fetchall():
                        list_id.append(elem[0])
                    if len(list_id) == 1:
                        list_id = list_id[0]
                        where_clauses.append(f' {key} = {list_id} ')
                    else:
                        list_id = tuple(list_id)
                        where_clauses.append(f' {key} IN {list_id} ')
            elif key == 'from':
                where_clauses.append(f' date >= ?')
                params.append(value)
            elif key == 'to':
                where_clauses.append(f' date <= ?')
                params.append(value)
            elif key == 'type' or key == 'account_id':
                where_clauses.append(f' {key} = ?')
                params.append(value)
            else:
                continue
    
        where_query = ''
        if where_clauses:
            where_query = 'WHERE {}'.format(' AND '.join(where_clauses))
        query = query_template.format(where_query=where_query)
        return query, params

    def get_report(self, account_id, dict_query=None):
        """ Обработка получения отчёта """
        cur = self.connection.cursor()
        filters = {'account_id': account_id}
        if dict_query:
            filters.update(dict_query)
        
        query, params = self.build_report_query(filters)
        select = """
        SELECT id, date, amount, type, comment, category_id
        FROM transactions
        """
        """Подсчёт total и item_count"""
        cur.execute(select + query, params)
        result = [dict(elem) for elem in cur.fetchall()]
        item_count = 0
        total = 0
        for elem in result:
            if elem['type'] == 'expenses':
                total -= float(elem['amount'])
            elif elem['type'] == 'income':
                total += float(elem['amount'])
            item_count += 1
        """Конструктор запроса LIMIT/OFFSET"""
        if 'page_size' in filters and int(filters["page_size"]) > 0:
            page_size = int(filters["page_size"])
        else:
            page_size = 20
    
        if 'page' in filters and int(filters["page"]) > 0:
            page = int(filters["page"])
        else:
            page = 1
        query = query + f'LIMIT {(page - 1) * page_size}, {page_size} '
        """Контрольный запрос получения транзакций с учётом пагинации"""
        cur.execute(select + query, params)
        transactions = [dict(elem) for elem in cur.fetchall()]
        for elem in transactions:
            category_id = elem.pop('category_id')
            if category_id:
                cur.execute(f"""
                    SELECT id, name
                    FROM categories
                    WHERE id = {category_id}
                """)
                elem['category'] = dict(cur.fetchone())
            else:
                elem['category'] = None
        if item_count % page_size > 0:
            page_count = item_count // page_size + 1
        else:
            page_count = item_count // page_size
        response = dict()
        response['page_count'] = page_count
        response['page'] = page
        response['page_size'] = page_size
        response['item_count'] = item_count
        response['total'] = f"{total:.2f}"
        response['transactions'] = transactions
    
        return response
    