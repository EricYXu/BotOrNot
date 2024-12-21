import math
import sqlite3
import torch
import os
from groq import Groq


""" GROQ API KEY"""
client = Groq(api_key="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",)

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

""" Obtain LLM response to the given prompt """
def get_bot_response(prompt):
    formal_prompt = prompt + " (limit response to 40 words)."

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": formal_prompt,
        }
    ],
    model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content
    
    

