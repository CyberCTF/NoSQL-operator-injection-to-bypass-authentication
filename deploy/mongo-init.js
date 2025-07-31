// MongoDB initialization script
// This script runs when the MongoDB container starts for the first time

// Switch to admin database
db = db.getSiblingDB('admin');

// Create admin user if it doesn't exist
if (!db.getUser("admin")) {
    db.createUser({
        user: "admin",
        pwd: "password123",
        roles: [
            { role: "userAdminAnyDatabase", db: "admin" },
            { role: "readWriteAnyDatabase", db: "admin" },
            { role: "dbAdminAnyDatabase", db: "admin" }
        ]
    });
    print("Admin user created successfully");
} else {
    print("Admin user already exists");
}

// Switch to shoppingnow database
db = db.getSiblingDB('shoppingnow');

// Create users collection and insert sample data
if (db.users.countDocuments({}) === 0) {
    db.users.insertMany([
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
    ]);
    print("Sample users inserted successfully");
} else {
    print("Users already exist in database");
}

print("MongoDB initialization completed"); 