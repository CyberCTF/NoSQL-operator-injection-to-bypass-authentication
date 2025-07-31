from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import json
import os
from datetime import datetime
import re
from pymongo import MongoClient

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'shoppingnow_secret_key_2024'

def load_metadata():
    """Load metadata from JSON file in deploy"""
    metadata_path = os.path.join(os.path.dirname(__file__), '..', 'deploy', 'metadata.json')
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "site": {"name": "ShoppingNow", "description": "Your trusted e-commerce platform"},
            "navigation": {"main": [], "auth": []},
            "footer": {"links": [], "social": []},
            "challenge": {"title": "Database Security Challenge", "description": "Description", "skills": [], "points": 0},
            "cta": {"label": "Start", "link": "/"}
        }

# MongoDB connection
def get_mongodb_client():
    """Get MongoDB client with connection to the database"""
    try:
        # Connect to MongoDB with authentication
        client = MongoClient('mongodb://admin:password123@mongodb:27017/', serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return None

def init_database():
    """Initialize the database connection"""
    client = get_mongodb_client()
    if client:
        print("MongoDB connection established successfully")
        return client
    return None

# Initialize database on startup
mongodb_client = init_database()

@app.route('/')
def home():
    metadata = load_metadata()
    return render_template('home.html', metadata=metadata)

@app.route('/customer-portal')
def customer_portal():
    if 'user' not in session:
        flash('Please log in to access the customer portal', 'error')
        return redirect(url_for('login'))
    
    user = session['user']
    return render_template('customer_portal.html', user=user, metadata=load_metadata())

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user' not in session:
        flash('Please log in to access the admin dashboard', 'error')
        return redirect(url_for('login'))
    
    user = session['user']
    if user.get('role') != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('customer_portal'))
    
    # Get admin data from MongoDB
    admin_data = {
        'total_users': 0,
        'total_orders': 0,
        'recent_activity': [
            {'action': 'User login', 'user': 'john_doe', 'time': '2024-01-15 10:30'},
            {'action': 'Order placed', 'user': 'jane_smith', 'time': '2024-01-15 09:15'},
            {'action': 'System backup', 'user': 'admin', 'time': '2024-01-15 08:00'}
        ]
    }
    
    if mongodb_client:
        db = mongodb_client.shoppingnow
        admin_data['total_users'] = db.users.count_documents({})
        admin_data['total_orders'] = sum(len(user.get('orders', [])) for user in db.users.find({}))
    
    return render_template('admin_dashboard.html', user=user, admin_data=admin_data, metadata=load_metadata())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if mongodb_client:
            db = mongodb_client.shoppingnow
            # Vulnerable query - directly uses user input without sanitization
            query = {"username": username, "password": password}
            user = db.users.find_one(query)
            
            if user:
                # Remove password and MongoDB ObjectId from session
                session_user = {k: v for k, v in user.items() if k not in ['password', '_id']}
                session['user'] = session_user
                
                if user['role'] == 'admin':
                    return jsonify({'success': True, 'redirect': '/admin-dashboard'})
                else:
                    return jsonify({'success': True, 'redirect': '/customer-portal'})
            else:
                return jsonify({'success': False, 'message': 'Invalid credentials'})
        else:
            return jsonify({'success': False, 'message': 'Database connection error'})
    
    metadata = load_metadata()
    return render_template('login.html', metadata=metadata)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('home'))

@app.route('/api/metadata')
def api_metadata():
    return jsonify(load_metadata())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 