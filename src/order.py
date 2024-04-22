from flask import Flask, jsonify
import psycopg2
from google.cloud import storage

app = Flask(__name__)

@app.route('/order', methods=['GET'])
def get_order():
    # Get the credentials from the Google Cloud Storage client.
    storage_client = storage.Client()
    credentials = storage_client._credentials

    # Use the credentials to establish a connection to the PostgreSQL database.
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password=credentials.service_account_email,
            service_account_path=credentials.service_account_file
        )

        # Create a cursor to execute queries.
        cursor = connection.cursor()

        # Execute a query to retrieve all orders from the database.
        cursor.execute('SELECT * FROM orders')

        # Fetch the results of the query.
        orders = cursor.fetchall()

        # Convert the results to JSON format.
        orders_json = jsonify(orders)

        # Close the cursor and the connection.
        cursor.close()
        connection.close()

        # Return the JSON response.
        return orders_json

    except (Exception, psycopg2.Error) as error:
        # Handle any errors that occur during the database connection or query execution.
        return jsonify({'error': str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True)
