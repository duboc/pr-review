from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/order1', methods=['POST'])
def create_order():
    data = request.get_json()
    return jsonify({'order': data}), 201

@app.route('/customer1', methods=['POST'])
def create_customer():
    data = request.get_json()
    return jsonify({'customer': data}), 201

@app.route('/product1', methods=['POST'])
def create_product():
    data = request.get_json()
    return jsonify({'product': data}), 201

@app.route('/address1', methods=['GET'])
def get_address():
    return jsonify({'address': '123 Main Street'}), 200

@app.route('/date1', methods=['GET'])
def get_date():
    return jsonify({'date': datetime.datetime.now().strftime('%Y-%m-%d')}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
