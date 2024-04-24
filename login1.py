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
    password = c.recv(1024)
    password = hashlib.sha512(password).hexdigest()

    with lock:
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()

        cur.execute("INSERT INTO USERS (USERNAME, EMAIL, PASSWORD) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        conn.close()

    c.send("User data saved successfully!".encode())

@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if re.search(email_condition, email):
            with lock:
                connection = sqlite3.connect('test.db')
                cursor = connection.cursor()

                cursor.execute("INSERT INTO USERS (USERNAME, EMAIL, PASSWORD) VALUES (?, ?, ?)", (username, email, password))
                connection.commit()
                connection.close()
                #c = client (parameter),c.send means the msg sent to client
#through sockets we can only send bytes, ?encoding, decoding to get the string
#hash the password to compare to the database
def handle_connection(c):
    c.send("Username:".encode())
    username = c.recv(1024).decode()
    c.send("Password:".encode())
    password = c.recv(1024)
    password = hashlib.sha512(password).hexdigest()
    
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?",(username, password))
    
    #if the login credentials acquired are correct, then
    if cur.fetchall():
        c.send("Login successful!".encode())
        #secrets, secret info
        #sevices that you want to add
    else:
        c.send("Login failed!".encode())

if __name__ == "__main__":
        # Test the email validation code
    user_email = input('Enter your Email : ')
    """if re.search(email_condition, user_email):
        print("Valid Email")
    else:
        print("Invalid Email")"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost",9999))
    server.listen()

    print("Server is listening...")

    while True:
        client, addr = server.accept()
        print(f"Connection from {addr} has been established.")
        threading.Thread(target=handle_connection, args=(client,)).start()

    app.run(debug=False)



"""
from flask import Flask, request, jsonify
import sqlite3
import hashlib
import socket
import threading
import re

app = Flask(__name__)

email_condition = "^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$"

def handle_connection(c):
    c.send("Username:".encode())
    username = c.recv(1024).decode()
    c.send("Password:".encode())
    password = c.recv(1024)
    password = hashlib.sha512(password).hexdigest()

    conn = sqlite3.connect("test.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?", (username, password))

    if cur.fetchall():
        c.send("Login successful!".encode())
    else:
        c.send("Login failed!".encode())

@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if re.search(email_condition, email):
            connection = sqlite3.connect('test.db')
            cursor = connection.cursor()

            cursor.execute("INSERT INTO USERS (USERNAME, EMAIL, PASSWORD) VALUES (?, ?, ?)", (username, email, password))
            connection.commit()

            connection.close()

            return jsonify({'message': 'User data saved successfully'})
        else:
            return jsonify({'message': 'Invalid email format'})

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost",9999))
    server.listen()
    # Test the email validation code
    user_email = input('Enter your Email : ')
    if re.search(email_condition, user_email):
        print("Valid Email")
    else:
        print("Invalid Email")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_connection, args=(client,)).start()

    app.run(debug=False)"""