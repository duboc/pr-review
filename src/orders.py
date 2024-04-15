from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password="mypassword"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer_id, product_id, quantity) VALUES (%s, %s, %s)", (data['customer_id'], data['product_id'], data['quantity']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Order created successfully'})

@app.route('/customer', methods=['POST'])
def create_customer():
    data = request.get_json()
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password="mypassword"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s)", (data['name'], data['email']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Customer created successfully'})

@app.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password="mypassword"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (data['name'], data['price']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product created successfully'})

if __name__ == '__main__':
    app.run(debug=True)
