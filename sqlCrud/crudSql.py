import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")
conn.commit()


def create_user():
    name = input('Enter Name: ')
    age = input("Enter Age: ")
    cursor.execute("INSERT INTO users (name,age) VALUES (?,?)",(name,age))
    conn.commit()
    print("User created successfully!\n")
    
def list_user():
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    if not rows:
        print("No users found.\n")
        return
    for row in rows:
        print(f"ID:{row[0]} | Name: {row[1]} | Age: {row[2]}")
    print()
    
def update_user():
    user_id = input("Enter user ID to update: ")
    new_name = input("Enter new name: ")
    new_age = input("Enter new age: ")
    cursor.execute("UPDATE users SET name = ?,age = ? WHERE id = ?",(new_name,new_age,user_id))
    conn.commit()
    if cursor.rowcount:
        print("User updated successfully!\n")
    else:
        print("User not found.\n")
        
def delete_user():
    user_id = input("Enter user id to delete: ")
    cursor.execute("DELETE FROM users WHERE id = ?",(user_id,))
    conn.commit()
    if cursor.rowcount:
        print("User deleted successfully!\n")
    else:
        print("User not found.\n")
        
def menu():
    while True:
        print("==== User CRUD App (SQLite) ====")
        print("1. Create user")
        print("2. List users")
        print("3. Update user")
        print("4. Delete user")
        print("5. Exit")
         
        choice = input("Choose an option (1-5): ")
        
        if choice == "1":
            create_user()
        elif choice == "2":
            list_user()
        elif choice == "3":
            update_user()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            print("Goodbye!")
            conn.close()  # close DB connection on exit
            break
        else:
            print("Invalid choice. Try again.\n")
            
menu()