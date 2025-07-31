// Initialize the shoppingnow database with test users
db = db.getSiblingDB('shoppingnow');

// Create users collection
db.createCollection('users');

// Insert test users
db.users.insertMany([
    {
        username: "john_doe",
        password: "password123",
        email: "john@example.com",
        role: "customer",
        created_at: new Date()
    },
    {
        username: "jane_smith",
        password: "jane123",
        email: "jane@example.com",
        role: "customer",
        created_at: new Date()
    },
    {
        username: "admin",
        password: "admin_secret_2024",
        email: "admin@shoppingnow.com",
        role: "admin",
        created_at: new Date()
    }
]);

// Create products collection
db.createCollection('products');

// Insert sample products
db.products.insertMany([
    {
        name: "Laptop Pro",
        price: 1299.99,
        description: "High-performance laptop for professionals",
        category: "Electronics",
        stock: 10,
        created_at: new Date()
    },
    {
        name: "Wireless Headphones",
        price: 199.99,
        description: "Premium noise-canceling headphones",
        category: "Electronics",
        stock: 25,
        created_at: new Date()
    },
    {
        name: "Smart Watch",
        price: 299.99,
        description: "Feature-rich smartwatch with health tracking",
        category: "Electronics",
        stock: 15,
        created_at: new Date()
    }
]);

print("Database initialized successfully!");
print("Users created: john_doe, jane_smith, admin");
print("Products created: Laptop Pro, Wireless Headphones, Smart Watch"); 