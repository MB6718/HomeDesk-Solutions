import sqlite3


with sqlite3.connect('db.sqlite') as connection:
    cursor = connection.cursor()

    cursor.executescript("""
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS accounts (
        id 		    INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name  TEXT    NOT NULL,
        last_name 	TEXT    NOT NULL,
        email 		TEXT    NOT NULL UNIQUE,
        password 	TEXT    NOT NULL
        );

        CREATE TABLE categories (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        parent_id   INTEGER NULL,
        account_id  INTEGER NOT NULL,
        name        TEXT    NOT NULL,
        FOREIGN KEY (account_id) REFERENCES account(id) ON DELETE CASCADE
        );
        
        CREATE TABLE transactions (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        date          INTEGER      NOT NULL,
        type          TEXT         NOT NULL,
        amount        TEXT         NOT NULL,
        comment       TEXT         NULL,
        category_id   INTEGER      NULL,
        account_id    INTEGER      NOT NULL,
        FOREIGN KEY (account_id) REFERENCES account(id) ON DELETE CASCADE
        )
    """)
