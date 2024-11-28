import sqlite3
from werkzeug.security import generate_password_hash


def create_connection():
    conn = sqlite3.connect("database.db")
    return conn


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role_id INTEGER,
        FOREIGN KEY (role_id) REFERENCES roles (id)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        subject TEXT NOT NULL,
        grade TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """
    )

    conn.commit()
    conn.close()


def add_user(firstname, lastname, username, password, role_id):
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    cursor.execute(
        "INSERT INTO users (firstname, lastname, username, password, role_id) VALUES (?, ?, ?, ?, ?)",
        (firstname, lastname, username, hashed_password, role_id),
    )
    conn.commit()
    conn.close()


def get_user(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def add_role(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO roles (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def get_roles():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    conn.close()
    return roles


def add_attendance(user_id, date, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO attendance (user_id, date, status) VALUES (?, ?, ?)",
        (user_id, date, status),
    )
    conn.commit()
    conn.close()


def get_attendance(user_id, date):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM attendance WHERE user_id = ? AND date = ?", (user_id, date)
    )
    attendance = cursor.fetchone()
    conn.close()
    return attendance


def get_attendance_by_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT date, status FROM attendance WHERE user_id = ?", (user_id,))
    attendance_records = cursor.fetchall()
    conn.close()
    return attendance_records


def update_attendance(user_id, date, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE attendance SET status = ? WHERE user_id = ? AND date = ?",
        (status, user_id, date),
    )
    conn.commit()
    conn.close()


def add_grade(user_id, subject, grade):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO grades (user_id, subject, grade) VALUES (?, ?, ?)",
        (user_id, subject, grade),
    )
    conn.commit()
    conn.close()


def initialize_roles():
    roles = ["student", "teacher"]
    conn = create_connection()
    cursor = conn.cursor()
    for role in roles:
        cursor.execute("SELECT * FROM roles WHERE name = ?", (role,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO roles (name) VALUES (?)", (role,))
    conn.commit()
    conn.close()


def get_students():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    students = cursor.fetchall()
    conn.close()
    return students
