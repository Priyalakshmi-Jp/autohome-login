import sqlite3
import hashlib
import socket 
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#This is TCP internet socket,connection-oriented protocol
server.bind(("localhost",9999))
#change the localhost to respective ip address with port
server.listen()

#c = client (parameter),c.send means the msg sent to client
#through sockets we can only send bytes, ∴encoding, decoding to get the string
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

while True:
    client, addr = server.accept()
    #to accept connection
    threading.Thread(target=handle_connection, args=(client,)).start()
    #client, is a mention for being a tuple
    
      
