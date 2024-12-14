import sqlite3
import hashlib
import os
import uuid


conn = sqlite3.connect('secure_login_system.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    department_id INTEGER,
    role_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sessions (
    session_token TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    FOREIGN KEY (username) REFERENCES users(username)
)
''')

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)  
    password_salt = password.encode('utf-8') + salt
    password_hash = hashlib.sha256(password_salt).hexdigest()
    return password_hash, salt


def generate_session_token():
    return str(uuid.uuid4())

def insert_departments_and_roles():

    departments = ['HR', 'Engineering', 'Marketing']
    for department in departments:
        cursor.execute("INSERT OR IGNORE INTO departments (name) VALUES (?)", (department,))
    
    roles = ['Admin', 'Manager', 'Employee']
    for role in roles:
        cursor.execute("INSERT OR IGNORE INTO roles (name) VALUES (?)", (role,))
    
    conn.commit()

def register_user():
    print("\n--- User Registration ---")
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    department_name = input("Enter department (HR, Engineering, Marketing): ")
    role_name = input("Enter role (Admin, Manager, Employee): ")


    cursor.execute("SELECT id FROM departments WHERE name=?", (department_name,))
    department_data = cursor.fetchone()
    if department_data is None:
        print(f"Department '{department_name}' does not exist. Please choose a valid department.")
        return

    cursor.execute("SELECT id FROM roles WHERE name=?", (role_name,))
    role_data = cursor.fetchone()
    if role_data is None:
        print(f"Role '{role_name}' does not exist. Please choose a valid role.")
        return

    department_id = department_data[0]
    role_id = role_data[0]

    password_hash, salt = hash_password(password)

    cursor.execute("INSERT INTO users (username, password_hash, salt, department_id, role_id) VALUES (?, ?, ?, ?, ?)", 
                   (username, password_hash, salt, department_id, role_id))
    conn.commit()

    print(f"User {username} successfully registered!\n")

def login():
    print("\n--- User Login ---")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT password_hash, salt, department_id, role_id FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()
    
    if user_data is None:
        print("Invalid username.")
        return None
    
    stored_hash, salt, department_id, role_id = user_data
    password_hash, _ = hash_password(password, salt)
    

    if password_hash == stored_hash:
        print(f"User {username} successfully authenticated!")
#tokens
        session_token = generate_session_token()
        cursor.execute("INSERT INTO sessions (session_token, username) VALUES (?, ?)", 
                       (session_token, username))
        conn.commit()
#dept
        cursor.execute("SELECT name FROM departments WHERE id=?", (department_id,))
        department_name = cursor.fetchone()[0]

        cursor.execute("SELECT name FROM roles WHERE id=?", (role_id,))
        role_name = cursor.fetchone()[0]

        print(f"Session created for {username}. Department: {department_name}, Role: {role_name}, Session token: {session_token}")
        return session_token
    else:
        print("Invalid password.")
        return None

def check_session(session_token):
    cursor.execute("SELECT username FROM sessions WHERE session_token=?", (session_token,))
    session_data = cursor.fetchone()
    
    if session_data:
        username = session_data[0]
        cursor.execute("SELECT department_id, role_id FROM users WHERE username=?", (username,))
        department_id, role_id = cursor.fetchone()

        cursor.execute("SELECT name FROM departments WHERE id=?", (department_id,))
        department_name = cursor.fetchone()[0]
        
        cursor.execute("SELECT name FROM roles WHERE id=?", (role_id,))
        role_name = cursor.fetchone()[0]
        
        print(f"Session is valid. Welcome back, {username} from {department_name} department, role: {role_name}!")
        return username, department_name, role_name
    else:
        print("Invalid session token.")
        return None

def main():
    insert_departments_and_roles()

    while True:
        print("\nWelcome to the Secure Login System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option (1/2/3): ")

        if choice == "1":
            register_user()
        elif choice == "2":
            session_token = login()
            if session_token:
                check_session(session_token)
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

conn.close()
