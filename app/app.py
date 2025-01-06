from flask import Flask, render_template, request, session
import sqlite3
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Initialize database
def init_db():
    conn = sqlite3.connect('responses.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            user_id TEXT,          
            response_id INTEGER,   
            response TEXT,
            PRIMARY KEY (user_id, response_id)
        )
    ''')
    conn.close()

def query_db():
    conn = sqlite3.connect('responses.db')
    rows = conn.execute('SELECT * FROM responses').fetchall()
    for row in rows:
        print(row)
    conn.close()

def clean_db():
    conn = sqlite3.connect('responses.db')
    conn.execute('DROP TABLE responses')
    conn.close()

@app.route('/')
def index():
    # Assign a unique user ID if not already assigned
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # Generate a unique user ID
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_id = session.get('user_id')
    if not user_id:
        return "User ID not found. Please reload the page."
    # Extract responses from the form
    responses = {
        1: request.form['response1'],  # response_id = 1
        2: request.form['response2'],  # response_id = 2
        3: request.form['response3']   # response_id = 3
    }

    conn = sqlite3.connect('responses.db')
    for response_id, response in responses.items():
        conn.execute('INSERT OR REPLACE INTO responses (user_id, response_id, response) VALUES (?, ?, ?)',
                     (user_id, response_id, response))
    conn.commit()
    conn.close()
    return f"Responses saved for User ID: {user_id}!"

if __name__ == '__main__':
    clean_db()
    init_db()
    app.run()
    query_db()
    

