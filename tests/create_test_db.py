import sqlite3


with sqlite3.connect('test-db.sqlite') as connection:
    cursor = connection.cursor()

    cursor.executescript("""
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS accounts (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name  TEXT    NOT NULL,
        last_name   TEXT    NOT NULL,
        email       TEXT    NOT NULL UNIQUE,
        password    TEXT    NOT NULL
        );

        CREATE TABLE categories (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        parent_id   INTEGER NULL,
        account_id  INTEGER NOT NULL,
        name        TEXT    NOT NULL,
        FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
        );
        
        CREATE TABLE transactions (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        date          INTEGER      NOT NULL,
        type          TEXT         NOT NULL,
        amount        TEXT         NOT NULL,
        comment       TEXT         NULL,
        category_id   INTEGER      NULL,
        account_id    INTEGER      NOT NULL,
        FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
        CONSTRAINT fk_categories
            FOREIGN KEY (category_id)
            REFERENCES categories(id)
            ON DELETE SET NULL
        )
    """)
    
    cursor.executescript("""
        INSERT INTO accounts (first_name, last_name, email, password)
        VALUES (
            "Max",
            "Bee",
            "maxbee@mail.com",
            "pbkdf2:sha256:150000$5CjSz8uh$9cf43ca444775449b22f0f7e4bb7d81340ef29736faf2dbb59a809f56bf4cec6"
        );
        
        INSERT INTO categories (parent_id, account_id, name)
        VALUES
            (NULL,  1,  "Еда"),
            (1,     1, "Продукты"),
            (2,     1, "Пятёрочка"),
            (3,     1, "Фрукты"),
            (4,     1, "Яблоки"),
            (4,     1, "Бананы"),
            (4,     1, "Апельсины"),
            (NULL,  1, "Одежда"),
            (8,     1, "Спортивная"),
            (9,     1, "Кроссовки"),
            (9,     1, "Футболки"),
            (9,     1, "Штаны"),
            (8,     1, "Нижнее бельё"),
            (NULL,  1, "Авто"),
            (14,    1, "Шиномонтаж"),
            (14,    1, "Бензин"),
            (14,    1, "Мойка"),
            (NULL,  1, "Работа"),
            (18,    1, "ЗП");
        
        INSERT INTO transactions (date, type, amount, comment, category_id, account_id)
        VALUES
            (1592815003, 'expenses',    '546.54',   'balbla uniq mark',                 NULL,   '1'),
            (1592825625, 'income',      '879.12',   'bonjur tujur abajur',              '1',    '1'),
            (1592838456, 'expenses',    '5465.10',  'tor gold fig mig',                 '1',    '1'),
            (1592872546, 'income',      '987.45',   'aurum quantum cephey',             '2',    '1'),
            (1593119557, 'expenses',    '423.32',   'aut sint velit',                   '2',   '1'),
            (1593219558, 'income',      '27.28',    'sint nam quam',                    '1',   '1'),
            (1593219736, 'expenses',    '280.38',   'et similique rerum',               '3',   '1'),
            (1593219737, 'income',      '821.81',   'sint numquam sit',                 '2',   '1'),
            (1593219738, 'expenses',    '413.91',   'debitis assumenda ad',             '3',   '1'),
            (1593319739, 'income',      '391.21',   'et quaerat ea',                    '8',   '1'),
            (1593319740, 'income',      '893.67',   'dolores debitis velit',            '9',   '1'),
            (1593319741, 'income',      '338.4',    'ipsa nihil qui',                   '6',   '1'),
            (1593320742, 'expenses',    '306.2',    'quia magni voluptas',              '4',   '1'),
            (1593320743, 'expenses',    '468.17',   'quibusdam accusantium nihil',      '6',   '1'),
            (1593420743, 'expenses',    '815.39',   'similique eius reprehenderit',     '9',   '1'),
            (1593420745, 'income',      '654.71',   'vitae aut aut',                    '10',   '1'),
            (1593420778, 'expenses',    '2.1',      'et quis omnis',                    '12',   '1'),
            (1593420779, 'expenses',    '572.26',   'nobis recusandae eum',             '4',   '1'),
            (1593420780, 'expenses',    '855.44',   'quos laborum qui',                 NULL,   '1'),
            (1593421781, 'expenses',    '601.27',   'necessitatibus voluptatum est',    '4',   '1'),
            (1593421782, 'income',      '902.84',   'molestias ipsum debitis',          '10',   '1'),
            (1593421782, 'expenses',    '333.83',   'aliquid vel ut',                   '9',   '1'),
            (1593421783, 'income',      '982.09',   'consequuntur error occaecati',     '7',   '1'),
            (1594418784, 'income',      '105.82',   'rerum illum vero',                 '10',   '1'),
            (1594419784, 'expenses',    '354.8',    'atque incidunt sit',               '4',   '1'),
            (1594419785, 'expenses',    '610.11',   'velit corrupti optio',             '8',   '1'),
            (1594421584, 'expenses',    '291.83',   'omnis velit sed',                  '9',   '1'),
            (1594421585, 'income',      '478.43',   'tempora nihil ut',                 '11',   '1'),
            (1594421586, 'income',      '168.77',   'adipisci nulla et',                '8',   '1'),
            (1594421587, 'income',      '592.77',   'veritatis quo cumque',             NULL,   '1'),
            (1594421588, 'expenses',    '744.84',   'aut numquam consequatur',          '17',   '1'),
            (1594421588, 'expenses',    '187.45',   'nihil accusantium ad',             '17',   '1'),
            (1594521589, 'income',      '502.22',   'aut tenetur reprehenderit',        '1',   '1'),
            (1594521590, 'expenses',    '768.34',   'quia ducimus est',                 '13',   '1'),
            (1594561590, 'income',      '723.01',   'dolores beatae natus',             '15',   '1'),
            (1594561591, 'income',      '133.29',   'sed necessitatibus quibusdam',     '14',   '1'),
            (1594561592, 'expenses',    '653.27',   'aspernatur aut reiciendis',        '8',   '1'),
            (1594561592, 'income',      '107.38',   'officiis voluptates tempora',      '16',   '1'),
            (1594561593, 'expenses',    '912.59',   'amet perferendis sint',            '2',   '1'),
            (1594561594, 'income',      '271.06',   'illo veritatis et',                '17',   '1'),
            (1594563802, 'expenses',    '405.72',   'eligendi ut atque',                '3',   '1'),
            (1594563820, 'income',      '57.07',    'quo quia ullam',                   '19',   '1');
    """)