import re
import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)
from flask_mysqldb import MySQL
import MySQLdb.cursors
from dotenv import dotenv_values
from utils.custom_log import get_custom_logger
from utils.create_folder_files import CreateFolderFile
config = dotenv_values(".env")

app = Flask(__name__)

app.secret_key = ' key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = config["host"]
app.config['MYSQL_USER'] = config["user"]
app.config['MYSQL_PASSWORD'] = config["password"]
app.config['MYSQL_DB'] = config["database"]

# Intialize MySQL
mysql = MySQL(app)

root_dir = os.path.dirname(os.path.abspath(__file__))
dir_logs = os.path.join(root_dir, 'logs')

logger = get_custom_logger(os.path.join(dir_logs, 'logs.log'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM from WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg='')

@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
    username = session["username"]
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    logger.info(f"Ha cerrado sesión el usuario {username}")
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/login/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM form WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            logger.info(f"Se ha registrado una cuenta para el usuario: {username}")
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/login/home', methods=['GET', 'POST'])
def home():
    username = request.form['username']
    session['loggedin'] = True
    #session['id'] = account['id']
    session['username'] = username
    logger.info(f"Ha iniciado sesión el usuario: {username}")
    return render_template('home.html', username=session['username'])

if __name__ == '__main__':
    
    print(root_dir)
    app.run(debug=True)