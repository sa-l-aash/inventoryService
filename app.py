from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

# Use environment variables or fallback values
db_config = {
    'user': os.environ.get('MYSQLUSER', 'root'),
    'password': os.environ.get('MYSQLPASSWORD', 'vtyiHJAehCLUpFHcqmWfhbfBPMYZdbdi'),
    'host': os.environ.get('MYSQLHOST', 'mysql.railway.internal'),
    'port': int(os.environ.get('MYSQLPORT', 3306)),
    'database': os.environ.get('MYSQLDATABASE', 'railway')
}


@app.route('/')
def index():
    return "[{"id":1,"name":"chair","price":9.99,"stock":30},{"id":2,"name":"Kettle","price":2.99,"stock":15}]"

@app.route('/products', methods=['GET'])
def get_products():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, stock, price) VALUES (%s, %s, %s)",
                       (data['name'], data['stock'], data['price']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': '✅ Product added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Required for Render
