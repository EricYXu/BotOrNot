import sqlite3

db_name = "site.db"
connection = sqlite3.connect(db_name)

cur = connection.cursor()

create_table_users = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    elo INTEGER NOT NULL DEFAULT 1500
);
"""

create_table_prompts = """
CREATE TABLE IF NOT EXISTS prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    text TEXT NOT NULL,
    elo INTEGER NOT NULL DEFAULT 1500
);
"""

create_table_bot = """
CREATE TABLE IF NOT EXISTS botText (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    text TEXT NOT NULL,
    elo INTEGER NOT NULL DEFAULT 1500
);
"""

create_table_human = """
CREATE TABLE IF NOT EXISTS humanText (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    text TEXT NOT NULL,
    elo INTEGER NOT NULL DEFAULT 0
);
"""

# Executes table creation
cur.execute(create_table_bot)
cur.execute(create_table_human)
cur.execute(create_table_users)
cur.execute(create_table_prompts)

# Inserts a few sample texts to get things started
cur.execute("INSERT INTO users (username,password,elo) VALUES (?, ?,?)",
            ('Eric','Test',0))
cur.execute("INSERT INTO prompts (username,text,elo) VALUES (?, ?,?)",
            ('Eric','What is a banana? (Limit response to 25 words)',0))
cur.execute("INSERT INTO humanText (username,text,elo) VALUES (?, ?,?)",
            ('Eric','A banana is an elongated, edible fruit produced by several kinds of large treelike herbaceous flowering plants in the genus Musa.',0))
cur.execute("INSERT INTO botText (username,text,elo) VALUES (?, ?,?)",
            ('Eric','A banana is a sweet, elongated fruit with a yellow peel, rich in potassium, commonly eaten raw or used in desserts and snacks.',0))

connection.commit()
connection.close()