from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
import sqlite3

app = Flask(__name__)

DATABASE = "user.db"

def get_db_conection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row #To use dict-style access 
    return conn
# Create users table if not exists
with get_db_conection() as conn:
       conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
        """)
       conn.commit()
       

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self,id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        conn = get_db_conection()
        user = conn.execute("SELECT * from users WHERE id=?",(user_id)).fetchone()
        conn.close()
        if user:
            return User(user["id"],user["username",user["password"]])
        return None
    
    @staticmethod
    def find_by_username(username):
        conn = get_db_conection()
        user = conn.execute("SELECT * from users WHERE username=?",(username,)).fetchone()
        conn.close()
        if user:
            return User(user["id"], user["username"], user["password"])
        return None
    
@login_manager.user_loader
def load_user(user_id):
        return User.get(user_id)