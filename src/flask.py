from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="my_password",
)
cursor = conn.cursor()

# Define the routes
@app.route('/order', methods=['POST'])
def create_order():
    # Get the order details from the request
    order_data = request.get_json()

    # Insert the order into the database
    cursor.execute(
        "INSERT INTO orders (product_id, customer_id, quantity) VALUES (%s, %s, %s)",
        (order_data['product_id'], order_data['customer_id'], order_data['quantity'])
    )
    conn.commit()

    # Return a success message
    return jsonify({'message': 'Order created successfully'})

@app.route('/customer', methods=['POST'])
def create_customer():
    # Get the customer details from the request
    customer_data = request.get_json()

    # Insert the customer into the database
    cursor.execute(
        "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
        (customer_data['name'], customer_data['email'], customer_data['phone'])
    )
    conn.commit()

    # Return a success message
    return jsonify({'message': 'Customer created successfully'})

@app.route('/product', methods=['POST'])
def create_product():
    # Get the product details from the request
    product_data = request.get_json()

    # Insert the product into the database
    cursor.execute(
        "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)",
        (product_data['name'], product_data['description'], product_data['price'])
    )
    conn.commit()

    # Return a success message
    return jsonify({'message': 'Product created successfully'})

if __name__ == '__main__':
    app.run(debug=True)
