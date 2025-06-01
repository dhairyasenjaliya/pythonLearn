import json
import os

DATA_FILE = "users.json"
users = []

def load_data():
    global users
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,'r') as f:
            users.extend(json.load(f))
            
def save_data():
    with open(DATA_FILE,"w") as f:
        json.dump(users,f,indent=4)

def create_user():
    name = input("Enter Name : ")
    age = input("Enter Age: ")
    
    user_id = len(users) + 1
    user = {
        "id":user_id,
        "name":name,
        "age":int(age)
    }
    users.append(user)
    save_data()
    print("User created successfully!\n")


def list_users():
    if not users:
        print("No users found.\n")
        return
    for user in users:  
        print(f"ID: {user['id']} | Name: {user['name']} | Age: {user['age']}")
    print()

def update_user():
    user_id = int(input("Enter a user ID to update: "))
    for user in users:
        if user["id"] == user_id:
            user["name"]= input("Enter new name: ")
            user["age"] = int(input("Enter new age: "))
            print("User updated successfully!\n")
            save_data()
            return
    print("User not found.\n")

def delete_user():
    user_id = int(input("Enter user ID to delete: "))
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            print("User deleted successfully!\n")
            save_data()
            return
    print("User not found.\n")
            
            
def menu():
    load_data()   
    while True:
        print("==== User CRUD App ====")
        print("1. Create user")
        print("2. List users")
        print("3. Update user")
        print("4. Delete user")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            update_user()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")
    
       
 
menu()