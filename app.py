from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

DB_NAME = "users.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Run only once to create the tables
def init_db():
    if not os.path.exists(DB_NAME):
        conn = get_db_connection()
        conn.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            );
        """)
        conn.commit()
        conn.close()

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        if user:
            return User(user["id"], user["username"], user["password"])
        return None

    @staticmethod
    def find_by_username(username):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user:
            return User(user["id"], user["username"], user["password"])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    conn = get_db_connection()
    entries = conn.execute("SELECT * FROM entries").fetchall()
    conn.close()
    return render_template("index.html", entries=entries)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.find_by_username(username):
            return "Username already exists!"
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.find_by_username(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        return "Invalid credentials!"
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        conn = get_db_connection()
        conn.execute("INSERT INTO entries (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add_user.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_user(id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM entries WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        conn.execute("UPDATE entries SET name = ?, age = ? WHERE id = ?", (name, age, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("edit_user.html", user=user)

@app.route("/delete/<int:id>")
@login_required
def delete_user(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM entries WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
