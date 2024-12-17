""" Update the site.db database using this script """

import sqlite3

db_name = "site.db"
connection = sqlite3.connect(db_name)
cur = connection.cursor()

# NOTE: SQL COMMANDS EXECUTED BELOW
# cur.execute("UPDATE prompts SET elo = ? WHERE id = ?", (1400,2))

# # Inserting prompts
# cur.execute("INSERT INTO prompts (username,text,elo) VALUES (?,?,?)",
#             ('Eric','What is the difference between a noun and a verb?',1400))
# cur.execute("INSERT INTO prompts (username,text,elo) VALUES (?,?,?)",
#             ('Eric',"What does the phrase 'supply and demand' mean in economics?",1400))
# cur.execute("INSERT INTO prompts (username,text,elo) VALUES (?,?,?)",
#             ('Eric','What is photosynthesis, and why is it important for plants?',1400))
# cur.execute("INSERT INTO prompts (username,text,elo) VALUES (?,?,?)",
#             ('Eric','What is the difference between a simile and a metaphor?',1400))

# # Inserting human responses
# cur.execute("INSERT INTO humanText (username,text,elo) VALUES (?,?,?)",
#             ('Eric',"Nouns are words that name persons, places, or things, and often serve as the subject or object of a verb. Verbs are words used to indicate actions, states, or relations between things.",1400))
# cur.execute("INSERT INTO humanText (username,text,elo) VALUES (?,?,?)",
#             ('Eric',"The law of supply and demand combines two fundamental economic principles that describe how changes in the price of a resource, commodity, or product affect its supply and demand. Supply rises while demand declines as the price increases. Supply constricts while demand grows as the price drops.",1400))
# cur.execute("INSERT INTO humanText (username,text,elo) VALUES (?,?,?)",
#             ('Eric',"Photosynthesis is a system of biological processes by which photosynthetic organisms, such as most plants, algae, and cyanobacteria, convert light energy, typically from sunlight, into the chemical energy necessary to fuel their metabolism.",1400))
# cur.execute("INSERT INTO humanText (username,text,elo) VALUES (?,?,?)",
#             ('Eric',"A simile is a comparison between two things that uses the word like or as: Her smile is as bright as sunshine. A metaphor is a direct comparison between two things that does not use like or as: Her smile is sunshine.",1400))

# # Inserting bot responses
# cur.execute("INSERT INTO botText (username,text,elo) VALUES (?,?,?)",
#             ('Eric',"A noun names a person, place, thing, or idea (e.g., dog, city). A verb describes an action or state of being (e.g., run, is). Nouns are 'what' or 'who,' while verbs are 'what happens' or 'what is.'",1400))
# cur.execute("INSERT INTO botText (username,text,elo) VALUES (?,?,?)",
#             ('Eric',"Supply and demand' refers to the relationship between the availability of a product (supply) and the desire for it (demand), which determines its price. Higher demand or lower supply raises prices, while lower demand or higher supply lowers them.",1400))
# cur.execute("INSERT INTO botText (username,text,elo) VALUES (?,?,?)",
#             ('Eric',"Photosynthesis is the process by which plants convert sunlight, water, and carbon dioxide into glucose (energy) and oxygen. It’s essential because it provides energy for plant growth and releases oxygen into the atmosphere, supporting life on Earth.",1400))
# cur.execute("INSERT INTO botText (username,text,elo) VALUES (?,?,?)",
#             ('Eric',"A simile compares two things using 'like' or 'as' (e.g., 'Her smile is like the sun'). A metaphor directly states one thing is another (e.g., 'Her smile is the sun'). Both highlight similarities but metaphors are more direct.",1400))

connection.commit()
connection.close()
