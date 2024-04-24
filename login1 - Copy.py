import threading
from flask import Flask, request, jsonify
import socket
import sqlite3
import hashlib
import re

app = Flask(__name__)

email_condition = "^[a-z]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
lock = threading.Lock()

def handle_connection(c):
    c.send("Username:".encode())
    username = c.recv(1024).decode()
    c.send("Email:".encode())
    email = c.recv(1024).decode()
    c.send("Password:".encode())
    password = c.recv(1024).decode()
    c.send("Confirm Password:".encode())
    confirm_password = c.recv(1024).decode()

    if password != confirm_password:
        c.send("Password and confirm password do not match!".encode())
        return

    if not re.search(email_condition, email):
        c.send("Invalid email format!".encode())
        return

    with lock:
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()

        # Check if username already exists
        cur.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
        if cur.fetchone():
            c.send("Username already exists!".encode())
            return

        # Insert new user data into the database
        cur.execute("INSERT INTO USERS (USERNAME, EMAIL, PASSWORD) VALUES (?, ?, ?)", (username, email, hashlib.sha512(password.encode()).hexdigest()))
        conn.commit()
        conn.close()

    c.send("User registered successfully!".encode())
        cur.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?",(username, password))
    
    #if the login credentials acquired are correct, then
    if cur.fetchall():
        c.send("Login successful!".encode())
        #secrets, secret info
        #sevices that you want to add
    else:
        c.send("Login failed!".encode())

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Connect to the database
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()

        # Check if the provided username and password match any user record in the database
        cursor.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?", (username, hashlib.sha512(password.encode()).hexdigest()))
        user = cursor.fetchone()

        conn.close()

        if user:
            return jsonify({'message': 'Login successful!'})
        else:
            return jsonify({'message': 'Invalid username or password'})


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            return jsonify({'message': 'Password and confirm password do not match!'})

        if not re.search(email_condition, email):
            return jsonify({'message': 'Invalid email format!'})

        with lock:
            connection = sqlite3.connect('test.db')
            cursor = connection.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
            if cursor.fetchone():
                return jsonify({'message': 'Username already exists!'})

            # Insert new user data into the database
            cursor.execute("INSERT INTO USERS (USERNAME, EMAIL, PASSWORD) VALUES (?, ?, ?)", (username, email, hashlib.sha512(password.encode()).hexdigest()))
            connection.commit()
            connection.close()

        return jsonify({'message': 'User registered successfully!'})

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost",9999))
    server.listen()

    print("Server is listening...")

    while True:
        client, addr = server.accept()
        print(f"Connection from {addr} has been established.")
        threading.Thread(target=handle_connection, args=(client,)).start()

    app.run(debug=False)


