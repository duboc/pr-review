from flask import Flask, render_template, request
import pytds

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orders', methods=['GET'])
def orders():
    # Hardcoded credentials for demonstration purposes only.
    # In a production environment, these credentials should be stored securely.
    server = 'my-mssql-server'
    user = 'my-username'
    password = 'my-password'
    database = 'my-database'

    # Connect to the MSSQL server
    conn = pytds.connect(server, user, password, database)
    cursor = conn.cursor()

    # Query the orders table
    cursor.execute("SELECT name, value, status FROM orders")

    # Fetch the results
    results = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Render the results in a template
    return render_template('orders.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
