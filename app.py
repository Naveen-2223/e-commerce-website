from flask import Flask, request, jsonify, session
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

app.secret_key = 'mysecretkey'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ecommerce'
mongo = PyMongo(app)

# ✅ Test route
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Flask backend is running!"})

# ✅ Seed products (resets and adds 2 products)
@app.route('/api/seed', methods=['GET'])
def seed_products():
    mongo.db.products.drop()  # Clear old products

    sample_products = [
        {
            'name': 'Blue T-Shirt',
            'price': 299,
            'description': '100% cotton T-shirt',
            'image_url': 'https://m.media-amazon.com/images/I/51s+IwY9XkL._AC_UL480_FMwebp_QL65_.jpg'
        },
        {
            'name': 'Red Hoodie',
            'price': 599,
            'description': 'Warm and stylish hoodie',
            'image_url': 'https://m.media-amazon.com/images/I/61fNn1eYI4L._AC_UL480_FMwebp_QL65_.jpg'
        }
    ]
    mongo.db.products.insert_many(sample_products)
    return jsonify({'message': 'Sample products added'}), 201

# ✅ Get all products
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = list(mongo.db.products.find())
        for p in products:
            p['_id'] = str(p['_id'])  # Convert ObjectId to string
        return jsonify(products)
    except Exception as e:
        print("🔥 Error in /api/products:", e)
        return jsonify({'error': str(e)}), 500

# ✅ Add product manually (if needed)
@app.route('/api/add_product', methods=['POST'])
def add_product():
    data = request.json
    product = {
        'name': data['name'],
        'price': float(data['price']),
        'description': data['description'],
        'image_url': data.get('image_url', '')
    }
    mongo.db.products.insert_one(product)
    return jsonify({'message': 'Product added'}), 201

# ✅ Add to cart
@app.route('/api/add_to_cart/<product_id>', methods=['GET'])
def add_to_cart(product_id):
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    return jsonify({'message': 'Added to cart'})

# ✅ View cart
@app.route('/api/cart', methods=['GET'])
def view_cart():
    try:
        ids = [ObjectId(id) for id in session.get('cart', [])]
        cart_items = list(mongo.db.products.find({'_id': {'$in': ids}}))
        for item in cart_items:
            item['_id'] = str(item['_id'])
        return jsonify(cart_items)
    except Exception as e:
        print("🔥 Error in /api/cart:", e)
        return jsonify({'error': str(e)}), 500

# ✅ Clear cart
@app.route('/api/clear_cart', methods=['GET'])
def clear_cart():
    session['cart'] = []
    return jsonify({'message': 'Cart cleared'})

if __name__ == '__main__':
    app.run(debug=True)
