from flask import Flask, render_template, request
import pytds

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orders', methods=['GET'])
def orders():
    # Load the service account credentials from a file
    credentials = pytds.Credentials.from_file('service-account.json')

    # Connect to the MSSQL server using the service account credentials
    conn = pytds.connect(server='my-mssql-server', credentials=credentials, database='my-database')
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
