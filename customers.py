from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Hardcoded password for PostgreSQL database
password = "123mudar"

# Define the connection parameters
connection_parameters = {
    "database": "dem",
    "user": "postgres",
    "password": password,
    "host": "10.81.224.3",
    "port": "5432",
}

# Create a connection to the PostgreSQL database
connection = psycopg2.connect(**connection_parameters)
cursor = connection.cursor()

# Define the routes
@app.route("/order", methods=["GET"])
def get_orders():
    """
    Get all orders from the database.
    """
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return jsonify(orders)

@app.route("/product", methods=["GET"])
def get_products():
    """
    Get all products from the database.
    """
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return jsonify(products)

@app.route("/customer", methods=["GET"])
def get_customers():
    """
    Get all customers from the database.
    """
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    return jsonify(customers)

if __name__ == "__main__":
    app.run(debug=True)
