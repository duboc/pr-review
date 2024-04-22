from flask import Flask, request
import mysql.connector

app = Flask(__name__)

@app.route('/order', methods=['GET'])
def get_order():
    order_id = request.args.get('order_id')

    # Hardcoded credentials for demonstration purposes only.
    # In a production environment, these credentials should be stored securely.
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='orders'
    )

    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM orders WHERE order_id={order_id}")
    order = cursor.fetchone()
    cursor.close()
    connection.close()

    return order

if __name__ == '__main__':
    app.run()
