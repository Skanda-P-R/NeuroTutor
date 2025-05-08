from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from groq_api_debug import get_code, compare
from symbolic_debugger import analyze_script, get_debugged_code
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('sql_username')
app.config['MYSQL_PASSWORD'] = os.getenv('sql_password')
app.config['MYSQL_DB'] = 'neuro_tutor_db'

mysql = MySQL(app)

@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html')
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
    try:
        errors = analyze_script(code_text)
        return jsonify({'errors': errors})
    except Exception as e:
        return jsonify({'errors': [f"Error in error checking: {str(e)}"]})

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