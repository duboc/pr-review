from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# Connect to the database
db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='password',
    db='my_database'
)

# Define the routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']

    # Insert the user into the database
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    db.commit()

    return render_template('success.html')

@app.route('/list_users')
def list_users():
    # Get all the users from the database
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    return render_template('list_users.html', users=users)

# Run the app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
