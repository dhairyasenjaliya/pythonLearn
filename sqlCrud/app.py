from flask import Flask, render_template, request, redirect, url_for
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
       
@app.route("/")
def index():
    conn = get_db_conection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template("index.html",users=users)

@app.route("/add",methods=["GET","POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        conn = get_db_conection()
        conn.execute("INSERT INTO users (name,age) VALUES (?,?)",(name,age))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add_user.html")

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit_user(id):
    conn = get_db_conection()
    user = conn.execute("SELECT * FROM users WHERE ID = ?",(id,)).fetchone()
    
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        conn.execute("UPDATE users SET name = ?, age = ? WHERE id = ?",(name,age,id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()
    return render_template("edit_user.html",user=user)

@app.route("/delete/<int:id>")
def delete_user(id): 
    conn = get_db_conection() 
    conn.execute("DELETE FROM users WHERE id = ?",(id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)