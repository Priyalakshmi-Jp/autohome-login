from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/',methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Connect to SQLite database
        connection = sqlite3.connect('test.db')
        cursor = connection.cursor()

        # Insert values into the database
        cursor.execute("INSERT INTO USERS (USERNAME, EMAIL, PASSWORD) VALUES (?, ?, ?)", (username, email, password))
        connection.commit()

        # Close database connection
        connection.close()

        return jsonify({'message': 'User data saved successfully'})

if __name__ == "__main__":
    app.run(debug=False)
