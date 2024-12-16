""" Update the site.db database using this script """

import sqlite3

db_name = "site.db"
connection = sqlite3.connect(db_name)
cur = connection.cursor()

update_table = """
UPDATE prompts
SET elo = '1400'
WHERE id = 1;
"""

cur.execute(update_table)
connection.commit()
connection.close()
