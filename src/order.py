from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Hardcoded credentials for PostgreSQL database
host = 'localhost'
database = 'postgres'
user = 'postgres'
password = 'my_password'

# Establish a connection to the PostgreSQL database
try:
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
except psycopg2.Error as e:
    print("Error connecting to PostgreSQL database: ", e)

# Define the routes for the Flask application

@app.route('/order', methods=['GET'])
def get_orders():
    """Get all orders from the database."""
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return jsonify(orders)

@app.route('/product', methods=['GET'])
def get_products():
    """Get all products from the database."""
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return jsonify(products)

@app.route('/customer', methods=['GET'])
def get_customers():
    """Get all customers from the database."""
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    return jsonify(customers)

if __name__ == '__main__':
    app.run(debug=True)
