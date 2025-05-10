from flask import Flask, render_template, request, redirect, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # use your DB username
app.config['MYSQL_PASSWORD'] = ''  # use your DB password
app.config['MYSQL_DB'] = 'user_auth'

mysql = MySQL(app)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                        (first_name, last_name, email, password))
            mysql.connection.commit()
            flash("Registration successful!", "success")
            return redirect('/login')
        except:
            flash("Email already exists.", "danger")
        finally:
            cur.close()
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[4], password):
            session['user'] = user[1]  # first name
            return f'<h1 style="color:red;">Welcome, {session['user']}!</h1>'
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
