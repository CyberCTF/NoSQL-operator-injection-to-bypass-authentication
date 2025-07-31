from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import json
import os
from datetime import datetime
import re

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

# Simulated MongoDB database with vulnerable query structure
class VulnerableMongoDB:
    def __init__(self):
        self.users = [
            {
                "username": "john_doe",
                "password": "password123",
                "email": "john@example.com",
                "role": "customer",
                "orders": ["ORD-001", "ORD-002"]
            },
            {
                "username": "admin",
                "password": "admin_secret_2024",
                "email": "admin@shoppingnow.com",
                "role": "admin",
                "permissions": ["manage_users", "view_analytics", "manage_orders"]
            },
            {
                "username": "jane_smith",
                "password": "jane123",
                "email": "jane@example.com",
                "role": "customer",
                "orders": ["ORD-003"]
            }
        ]
    
    def find_one(self, query):
        """Vulnerable find_one method that directly evaluates query operators"""
        # This is intentionally vulnerable - it processes MongoDB-like operators
        for user in self.users:
            match = True
            for key, value in query.items():
                if key == "username":
                    if isinstance(value, dict):
                        # Handle MongoDB operators
                        if "$ne" in value:
                            if user["username"] == value["$ne"]:
                                match = False
                        elif "$regex" in value:
                            pattern = value["$regex"]
                            if not re.search(pattern, user["username"]):
                                match = False
                    else:
                        if user["username"] != value:
                            match = False
                elif key == "password":
                    if isinstance(value, dict):
                        # Handle MongoDB operators
                        if "$ne" in value:
                            if user["password"] == value["$ne"]:
                                match = False
                        elif "$regex" in value:
                            pattern = value["$regex"]
                            if not re.search(pattern, user["password"]):
                                match = False
                    else:
                        if user["password"] != value:
                            match = False
            if match:
                return user
        return None

# Initialize vulnerable database
db = VulnerableMongoDB()

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
    
    # Admin-specific data
    admin_data = {
        'total_users': len(db.users),
        'total_orders': sum(len(user.get('orders', [])) for user in db.users),
        'recent_activity': [
            {'action': 'User login', 'user': 'john_doe', 'time': '2024-01-15 10:30'},
            {'action': 'Order placed', 'user': 'jane_smith', 'time': '2024-01-15 09:15'},
            {'action': 'System backup', 'user': 'admin', 'time': '2024-01-15 08:00'}
        ]
    }
    
    return render_template('admin_dashboard.html', user=user, admin_data=admin_data, metadata=load_metadata())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Vulnerable query - directly uses user input without sanitization
        query = {"username": username, "password": password}
        user = db.find_one(query)
        
        if user:
            # Remove password from session
            session_user = {k: v for k, v in user.items() if k != 'password'}
            session['user'] = session_user
            
            if user['role'] == 'admin':
                return jsonify({'success': True, 'redirect': '/admin-dashboard'})
            else:
                return jsonify({'success': True, 'redirect': '/customer-portal'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    
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