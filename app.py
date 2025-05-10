from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from groq_api_debug import get_code, compare
from symbolic_debugger import analyze_script, get_debugged_code
import os
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('sql_username')
app.config['MYSQL_PASSWORD'] = os.getenv('sql_password')
app.config['MYSQL_DB'] = 'neuro_tutor_db'

mysql = MySQL(app)

ALL_MILESTONES = {
    "codes_corrected": {
        5: "Code Fixer I",
        10: "Code Fixer II",
        20: "Syntax Surgeon"
    },
    "coins": {
        1: "First Login",
        5: "Coin Collector I",
        10: "Coin Collector II",
        25: "Coin Collector III"
    },
    "questions_debugged": {
        1: "First Debug",
        5: "Debug Mastery I",
        10: "Debug Mastery II",
        25: "Bug Slayer"
    }
}

def assign_badges(email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, questions_debugged, codes_corrected, coins FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    user_id = user['id']
    codes_corrected = user['codes_corrected']
    questions_debugged = user.get('questions_debugged', 0)
    coins = user['coins']
    badge_to_show = None

    for field, milestones in ALL_MILESTONES.items():
        current_value = user[field]
        for milestone, badge_name in milestones.items():
            if current_value >= milestone:
                cursor.execute("SELECT id FROM badges WHERE name = %s", (badge_name,))
                cursor.execute("SELECT id, name, description, icon_filename FROM badges WHERE name = %s", (badge_name,))
                badge = cursor.fetchone()

                if badge:
                    badge_id = badge['id']
                    cursor.execute("SELECT * FROM user_badges WHERE user_id = %s AND badge_id = %s", (user_id, badge_id))
                    if not cursor.fetchone():
                        cursor.execute("INSERT INTO user_badges (user_id, badge_id, awarded_on) VALUES (%s, %s, NOW())",
                                       (user_id, badge_id))
                        mysql.connection.commit()
                        badge_to_show = badge
                        break
        if badge_to_show:
            break
    return badge_to_show

@app.route('/')
def index():
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT coins FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        coins = user['coins']
        badge_to_show = assign_badges(email)
        return render_template('index.html', coins=coins, badge_to_show=badge_to_show)
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['email'] = user['email']

            ist = pytz.timezone('Asia/Kolkata')
            now = datetime.now(ist)
            if now.hour < 5:
                today_5am = now.replace(hour=5, minute=0, second=0, microsecond=0) - timedelta(days=1)
            else:
                today_5am = now.replace(hour=5, minute=0, second=0, microsecond=0)

            last_award = user.get('last_coin_award')
            if last_award and not last_award.tzinfo:
                last_award = ist.localize(last_award)
            if not last_award or last_award < today_5am:
                cursor.execute("""
                    UPDATE users 
                    SET coins = coins + 1, last_coin_award = %s 
                    WHERE email = %s
                """, (now, email))
                mysql.connection.commit()
            return redirect('/')
        else:
            error = 'Incorrect email or password!'
    
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            error = 'User already exists!'
        else:
            error = 'User Created Successfully, Login Now!'
            cursor.execute(
                'INSERT INTO users (email, password) VALUES (%s, %s)',
                (email, hashed_password)
            )   
            mysql.connection.commit()
            return render_template('login.html',error=error)

    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

@app.route('/code-checker')
def code_checker():
    if 'email' in session:
        return render_template("code.html")
    return redirect('/login')

@app.route('/debugger-challenge')
def debugger_challenge():
    if 'email' in session:
        return render_template("debug.html")
    return redirect('/login')

@app.route('/my-badges')
def my_badges():
    if 'email' in session:
        email = session['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, coins FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        user_id = user['id']
        coins = user['coins']
        cursor.execute("""
            SELECT b.name AS title, b.description, b.icon_filename, ub.awarded_on
            FROM user_badges ub
            JOIN badges b ON ub.badge_id = b.id
            WHERE ub.user_id = %s
            ORDER BY ub.awarded_on DESC
        """, (user_id,))
        badges = cursor.fetchall()
        return render_template('my_badges.html', badges=badges, coins=coins)
    return redirect('/login')

@app.route("/get_code", methods=["POST"])
def fetch_code():
    data = request.get_json()
    difficulty = data.get("difficulty")
    code = get_code(difficulty)
    return jsonify({"code": code})

@app.route("/check_solution", methods=["POST"])
def check_solution():
    data = request.get_json()
    error_code = data.get("error_code")
    user_code = data.get("user_code")
    result = compare(error_code, user_code)
    if 'email' in session:
        if "good job debugging all errors!" in result.lower():
            result = "Good job debugging all errors!"
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE users SET questions_debugged = questions_debugged + 1 WHERE email = %s", (session['email'],))
            mysql.connection.commit()
    return jsonify({"result": result})

@app.route('/check_errors', methods=['POST'])
def check_errors():
    code_text = request.json.get('code', '')
    errors = analyze_script(code_text)
    return jsonify({'errors': errors})

@app.route('/correct_code', methods=['POST'])
def correct_code():
    code_text = request.json.get('code', '')
    errors = request.json.get('errors', [])
    try:
        corrected_code = get_debugged_code(errors, code_text)
        if 'email' in session:
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE users SET codes_corrected = codes_corrected + 1 WHERE email = %s", (session['email'],))
            mysql.connection.commit()
        return jsonify({'corrected_code': corrected_code})
    except Exception as e:
        return jsonify({'error': f"Error in code correction: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)