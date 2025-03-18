from flask import Flask, request, Response
import psycopg2
import os
import json
from flask_cors import CORS  # Add this import

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Rest of your code remains unchanged


# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "ecommerce_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "post_gre_password")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

# Simple route to test the API
@app.route('/')
def hello():
    return Response("Welcome to our simple Flask e-commerce backend!", status=200, mimetype="text/plain")

# Endpoint to initialize the database (create products table)
@app.route('/init-db')
def init_db():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10,2) NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()

        return Response("Database initialized successfully!", status=200, mimetype="text/plain")
    except Exception as e:
        print(e)
        return Response("Error initializing the database.", status=500, mimetype="text/plain")

# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name, price FROM products")
        rows = cur.fetchall()

        products = [{"id": row[0], "name": row[1], "price": str(row[2])} for row in rows]

        cur.close()
        conn.close()
        return Response(json.dumps(products), status=200, mimetype="application/json")
    except Exception as e:
        print(e)
        return Response("Error fetching products.", status=500, mimetype="text/plain")

# Add a new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    if not data or 'name' not in data or 'price' not in data:
        return Response("Invalid request data", status=400, mimetype="text/plain")

    name = data['name']
    price = data['price']

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id, name, price",
            (name, price)
        )
        new_product = cur.fetchone()
        conn.commit()

        product_obj = {"id": new_product[0], "name": new_product[1], "price": str(new_product[2])}

        cur.close()
        conn.close()
        return Response(json.dumps(product_obj), status=201, mimetype="application/json")
    except Exception as e:
        print(e)
        return Response("Error adding product.", status=500, mimetype="text/plain")

# Delete a product by ID
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        rows_deleted = cur.rowcount
        conn.commit()

        cur.close()
        conn.close()

        if rows_deleted > 0:
            return Response(f"Product with ID {product_id} deleted.", status=200, mimetype="text/plain")
        else:
            return Response(f"No product found with ID {product_id}.", status=404, mimetype="text/plain")
    except Exception as e:
        print(e)
        return Response("Error deleting product.", status=500, mimetype="text/plain")

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
