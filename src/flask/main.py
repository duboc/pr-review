from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()
    return jsonify({'order': data}), 201

@app.route('/customer', methods=['POST'])
def create_customer():
    data = request.get_json()
    return jsonify({'customer': data}), 201

@app.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()
    return jsonify({'product': data}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
