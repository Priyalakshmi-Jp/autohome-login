import sqlite3
import hashlib

conn = sqlite3.connect("test.db")
cur = conn.cursor()

username1,email1, password1 ="Priya", "priya@gmail.com", hashlib.sha512("hjkl123".encode()).hexdigest()
username2,email2, password2 ="Smitha","smitha@gmail.com", hashlib.sha512("werfds123".encode()).hexdigest()
username3,email3, password3 ="devi","devi@gmail.com", hashlib.sha512("dfghj123".encode()).hexdigest()
username4,email4, password4 ="abhinav", "Abhinav@gmail.com", hashlib.sha512("dfghj234".encode()).hexdigest()
cur.execute("INSERT INTO USERS(username,password,email) VALUES (?,?,?)",(username1,password1,email1))
cur.execute("INSERT INTO USERS(username,password,email) VALUES (?,?,?)",(username2,password2,email4))
cur.execute("INSERT INTO USERS(username,password,email) VALUES (?,?,?)",(username3,password3,email3))
cur.execute("INSERT INTO USERS(username,password,email) VALUES (?,?,?)",(username4,password4,email4))
conn.commit()
#print(password1)
