from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

# Use environment variables for config (recommended on Render)
db_config = {
    'user': os.environ.get('DB_USER', 'flask_user'),
    'password': os.environ.get('DB_PASSWORD', 'ASKprime123456789.COM'),
    'host': os.environ.get('DB_HOST', 'localhost'),  # Update this to your actual host on Render
    'port': int(os.environ.get('DB_PORT', 3308)),
    'database': os.environ.get('DB_NAME', 'inventory_db')
}

@app.route('/')
def index():
    return "✅ Welcome to Inventory Service!"

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
    app.run(debug=True, host='0.0.0.0', port=5000)  # Port 5000 is required by Render
