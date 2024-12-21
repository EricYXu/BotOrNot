import os
from flask import Flask, request, redirect, render_template, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import random
from helpers import get_db_connection, change_elo, get_bot_response

# Configuring Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

""" Home """
@app.route('/')
def index():
    return render_template('home.html')

""" Tutorial """
@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

""" Landing """
@app.route("/landing", methods=["GET", "POST"])
def landing():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return render_template("landing.html", user=user)

""" Game """
@app.route('/game', methods=["GET", "POST"])
def game():
    if "user_id" not in session:
        flash('Please create an account first.')
        return redirect("/")

    # Gets user information
    user_id = session["user_id"]
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    # Formats the game
    format = random.randint(1,2)
    promptIndices = conn.execute('SELECT COUNT(*) AS prompt_count FROM prompts').fetchone()['prompt_count']
    promptIndex = random.randint(1,promptIndices)
    prompt = conn.execute('SELECT * FROM prompts WHERE id = ?',(promptIndex,)).fetchone()

    if format == 1:
        """ Bot Human """
        text1 = prompt['botText']
        text2 = prompt['humanText']
    else:
        """ Human Bot """
        text1 = prompt['humanText']
        text2 = prompt['botText']

    """ Game Logic """
    if request.method == 'POST':
        response1 = request.form.get('response1')
        print(response1)
        justification = request.form.get('justification')

        if not response1:
            flash('Enter a valid guess.')
            return render_template("game.html",text1=text1, text2=text2, prompt=prompt,user=user)
        elif not justification:
            flash('Enter a valid justification.')
            return render_template("game.html",text1=text1, text2=text2, prompt=prompt,user=user)

        numberCorrect = 0
        if format == 1:
            if response1 == "bot-human":
                numberCorrect = 1
            else:
                numberCorrect = 0
        else:
            if response1 == "human-bot":
                numberCorrect = 1
            else:
                numberCorrect = 0

        new_score = numberCorrect + user['questionsCorrect']

        # Obtains the new elo of the player and prompt, updates using SQL commands
        new_player_elo = user['elo'] + change_elo(user['elo'], prompt['elo'], numberCorrect)
        new_prompt_elo = prompt['elo'] - change_elo(user['elo'], prompt['elo'], numberCorrect)
        conn.execute("UPDATE users SET elo = ? WHERE id = ?", (new_player_elo,user_id))
        conn.execute("UPDATE users SET questionsCorrect = ? WHERE id = ?", (new_score,user_id))
        conn.execute("UPDATE prompts SET elo = ? WHERE id = ?", (new_prompt_elo,promptIndex))
        conn.execute("INSERT INTO justifications (username, promptID, justification) VALUES (?,?,?)",
                        (user['username'],promptIndex,justification))

    # Commits changes, closes database connection
    conn.commit()
    conn.close()

    return render_template('game.html',text1=text1, text2=text2, prompt=prompt,user=user)

""" Insert """
@app.route('/insert', methods=["GET", "POST"])
def insert():
    if "user_id" not in session:
        flash('Please create an account first.')
        return redirect("/")

    # Gets user information
    user_id = session["user_id"]
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if request.method == "POST":
        # update sql table, check for injection, cleanse data
        prompt = request.form.get('prompt')
        human_response = request.form.get('human')
        bot_response = get_bot_response(prompt)

        # SQL command to insert into the database
        conn = get_db_connection()
        conn.execute("INSERT INTO prompts (username, promptText, humanText, botText) VALUES (?,?,?,?)",(user['username'], prompt, human_response, bot_response))
        conn.commit()
        conn.close()

        flash('Successfully added prompt!')
        return render_template("insert.html")
    else:
        return render_template("insert.html")
    
""" Leaderboard """
@app.route('/leaderboard', methods=["GET", "POST"])
def leaderboard():
    conn = get_db_connection()
    rankedUsers = conn.execute("SELECT * FROM users ORDER BY elo DESC").fetchall()
    rankedPrompts = conn.execute("SELECT * FROM prompts ORDER BY elo DESC").fetchall()
    return render_template("leaderboard.html", rankedUsers=rankedUsers, rankedPrompts=rankedPrompts)

""" Login: Eric,Test  NicolasBourbaki,Test2 """
@app.route('/login', methods=["GET", "POST"])
def login():
    session.clear()
    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "POST":
        # Check validity of fields
        if not username:
            flash('Enter a valid username.')
            return render_template("login.html")
        elif not password:
            flash('Enter a valid password.')
            return render_template("login.html")

        # Query database for username
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        conn.close()
        
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash('Invalid username or password.')
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        flash('Successfully logged in!')
        return redirect("/landing")
    else:
        return render_template("login.html")

""" Register """
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username:
            flash('Enter a valid username.')
            return render_template("register.html")
        elif not password:
            flash('Enter a valid password and confirmation.')
            return render_template("register.html")
        elif not confirmation:
            flash('Enter a valid password and confirmation.')
            return render_template("register.html")
        elif password != confirmation:
            flash('Ensure password and confirmation match.')
            return render_template("register.html")
        else:
            # TODO: REJECT DUPLICATE USERNAMES
            conn = get_db_connection()
            rows = conn.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        
            if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
                flash('Username already taken.')
                return render_template("register.html")

            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                        (username, generate_password_hash(password)))
            conn.commit()
            conn.close()

        flash('Account created successfully.')
        return redirect("/")
    else:
        return render_template("register.html")

""" Logout """
@app.route("/logout")
def logout():
    """ Logs user out """
    session.clear()
    flash('Successfully logged out.')
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)