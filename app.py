from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Database configuration
server = 'dbserverpython.database.windows.net'
database = 'profile'
username = 'solai'
password = 'admin@123'
driver = '{ODBC Driver 17 for SQL Server}'

def create_table_if_not_exists():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Contacts')
        CREATE TABLE Contacts (
            ID INT PRIMARY KEY IDENTITY,
            Name NVARCHAR(255),
            Email NVARCHAR(255),
            Subject NVARCHAR(255),
            Message NVARCHAR(MAX)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['POST'])
def contact_form():
    create_table_if_not_exists()

    data = request.get_json()
    print(data)
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    # Connect to the database
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()

    # Insert data into the database
    cursor.execute('INSERT INTO Contacts (Name, Email, Subject, Message) VALUES (?, ?, ?, ?)', name, email, subject, message)
    conn.commit()

    conn.close()

    return jsonify({"message": "Thank you for submitting the form!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
