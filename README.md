# Bypass Authentication via MongoDB NoSQL Operator Injection

Learn to exploit MongoDB operator injection in a login form to authenticate as an admin without valid credentials.

## Overview

This lab demonstrates a real-world NoSQL injection vulnerability in a Flask-based e-commerce application. The ShoppingNow platform uses a vulnerable MongoDB query structure that allows attackers to bypass authentication using MongoDB operators like `$ne` and `$regex`.

## Objectives

- Identify NoSQL injection vectors in authentication endpoints
- Craft payloads using MongoDB operators ($ne and $regex)
- Bypass authentication to gain admin access

## Difficulty

**Beginner**

## Estimated Time

20-30 minutes

## Prerequisites

- Basic web application penetration testing
- Familiarity with MongoDB query syntax
- Burp Suite or similar proxy tool

## Skills Learned

- Finding and exploiting NoSQL injection vulnerabilities
- Crafting JSON injection payloads
- Authentication bypass strategies

## Project Structure

```
├── build/
│   ├── web/                 # Flask application
│   │   ├── app.py          # Main Flask application
│   │   ├── requirements.txt # Python dependencies
│   │   ├── templates/      # HTML templates
│   │   ├── static/         # Static assets
│   │   └── Dockerfile      # Web container definition
│   └── db/
│       └── init/           # MongoDB initialization scripts
├── deploy/
│   ├── docker-compose.yaml # Production Docker configuration
│   ├── Dockerfile         # Container definition
│   └── metadata.json      # Application metadata
├── docs/
│   └── WRITEUP.md         # Detailed exploitation guide
├── test/
│   ├── test_lab.py        # Automated tests
│   └── requirements.txt   # Test dependencies
└── README.md              # This file
```

## Quick Start

### Prerequisites
- Docker
- Python 3.11+
- Burp Suite Community Edition

### Development Setup
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up --build

# Access the application
# Web: http://localhost:3206
# MongoDB: localhost:27017
```

### Production Setup
```bash
# Start production environment
cd deploy
docker-compose up --build
```

## Demo Accounts

- **Customer:** john_doe / password123
- **Customer:** jane_smith / jane123
- **Admin:** admin / admin_secret_2024 (hidden account)

## Vulnerability Details

The application uses a vulnerable MongoDB query structure in the login endpoint:

```python
# Vulnerable query - directly uses user input without sanitization
query = {"username": username, "password": password}
user = db.users.find_one(query)
```

The `find_one` method processes MongoDB operators directly, allowing injection attacks.

## Testing

Run the automated tests to verify the vulnerability:

```bash
cd test
pip install -r requirements.txt
python test_lab.py
```

Or run with pytest:

```bash
pytest test_lab.py -v
```

## Flag

The flag is displayed in the admin dashboard after successful exploitation:
`FLAG{NoSQL_1nj3ct10n_4dm1n_byp4ss_2024}`

## ARM Compatibility

This lab is compatible with ARM architectures (Apple Silicon, ARM64) using MongoDB 4.4 which doesn't require AVX support.

## Issue Tracker

Report issues at: https://github.com/your-org/shoppingnow-lab/issues

---

*This is a deliberately vulnerable lab designed solely for educational purposes.* 