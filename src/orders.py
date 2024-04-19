from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Hardcoded credentials for PostgreSQL database
host = 'localhost'
database = 'postgres'
user = 'postgres'
password = 'my_password'

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)
cursor = conn.cursor()

# Define the routes for the API

@app.route('/order', methods=['GET'])
def get_orders():
    # Execute a query to retrieve all orders from the database
    cursor.execute('SELECT * FROM orders')
    
    # Fetch the results of the query
    orders = cursor.fetchall()
    
    # Convert the results to JSON format
    orders_json = jsonify(orders)
    
    # Return the JSON response
    return orders_json

@app.route('/customer', methods=['GET'])
def get_customers():
    # Execute a query to retrieve all customers from the database
    cursor.execute('SELECT * FROM customers')
    
    # Fetch the results of the query
    customers = cursor.fetchall()
    
    # Convert the results to JSON format
    customers_json = jsonify(customers)
    
    # Return the JSON response
    return customers_json

@app.route('/product', methods=['GET'])
def get_products():
    # Execute a query to retrieve all products from the database
    cursor.execute('SELECT * FROM products')
    
    # Fetch the results of the query
    products = cursor.fetchall()
    
    # Convert the results to JSON format
    products_json = jsonify(products)
    
    # Return the JSON response
    return products_json

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
