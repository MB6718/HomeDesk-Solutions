import sqlite3


with sqlite3.connect('test-db.sqlite') as connection:
	cursor = connection.cursor()

	cursor.executescript("""
		PRAGMA foreign_keys = ON;
		CREATE TABLE IF NOT EXISTS accounts (
		id			INTEGER PRIMARY KEY AUTOINCREMENT,
		first_name	TEXT	NOT NULL,
		last_name	TEXT	NOT NULL,
		email		TEXT	NOT NULL UNIQUE,
		password	TEXT	NOT NULL
		);

		CREATE TABLE categories (
		id			INTEGER PRIMARY KEY AUTOINCREMENT,
		parent_id	INTEGER NULL,
		account_id	INTEGER NOT NULL,
		name		TEXT	NOT NULL,
		FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
		);
		
		CREATE TABLE transactions (
		id			  INTEGER PRIMARY KEY AUTOINCREMENT,
		date		  INTEGER	   NOT NULL,
		type		  TEXT		   NOT NULL,
		amount		  TEXT		   NOT NULL,
		comment		  TEXT		   NULL,
		category_id	  INTEGER	   NULL,
		account_id	  INTEGER	   NOT NULL,
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
			(NULL, 1, "еда"),
			(1,	1, "продукты"),
			(2,	1, "пятёрочка"),
			(3,	1, "плюшки");
		
		INSERT INTO transactions (date, type, amount, comment, category_id, account_id)
		VALUES
			(1592815003, "expenses", "546.54", "balbla uniq mark", NULL, 1),
			(1592825625, "income", "879.12", "bonjur tujur abajur", 1, 1),
			(1592838456, "expenses", "5465.10", "tor gold fig mig", 2, 1),
			(1592872546, "income", "987.45", "aurum quantum cephey", 3, 1);
	""")