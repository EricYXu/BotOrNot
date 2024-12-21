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
    elo INTEGER NOT NULL DEFAULT 1500,
    questionsCorrect INTEGER NOT NULL DEFAULT 0
);
"""

create_table_prompts = """
CREATE TABLE IF NOT EXISTS prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    promptText TEXT NOT NULL,
    humanText TEXT NOT NULL,
    botText TEXT NOT NULL,
    elo INTEGER NOT NULL DEFAULT 1500,
    votes INTEGER NOT NULL DEFAULT 0
);
"""

create_table_justifications = """
CREATE TABLE IF NOT EXISTS justifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    promptID INTEGER NOT NULL,
    justification TEXT NOT NULL
);
"""

# Executes table creation
cur.execute(create_table_justifications)
# cur.execute(create_table_prompts)

# Inserts a few sample texts to get things started
# cur.execute("INSERT INTO prompts (username,promptText,humanText,botText) VALUES (?,?,?,?)",
#             ('Eric','What is a banana?','A banana is an elongated, edible fruit produced by several kinds of large treelike herbaceous flowering plants in the genus Musa.','A banana is a sweet, elongated fruit with a yellow peel, rich in potassium, commonly eaten raw or used in desserts and snacks.'))

connection.commit()
connection.close()