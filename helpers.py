import requests
import math
import sqlite3
# from flask import redirect, render_template, session
# from functools import wraps

# """ Checks if login is required to reach this page"""
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get("user_id") is None:
#             return redirect("/login")
#         return f(*args, **kwargs)

#     return decorated_function

""" Connects to database """
def get_db_connection():
    conn = sqlite3.connect('site.db')
    conn.row_factory = sqlite3.Row
    return conn

""" Changes the elo of a player after a game """
def change_elo(playerELO, promptELO, score):
    kfactor = 20.0
    diff = (playerELO - promptELO)/400
    expectedScore = 1.0 / (math.pow(10, diff) + 1)
    eloChange = kfactor * (score - expectedScore)
    rounded_eloChange = round(eloChange)
    return rounded_eloChange
