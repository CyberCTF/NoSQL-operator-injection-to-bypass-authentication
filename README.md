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
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── templates/            # HTML templates
│   └── static/              # Static assets
├── deploy/
│   ├── docker-compose.yaml   # Docker configuration
│   ├── Dockerfile           # Container definition
│   └── metadata.json        # Application metadata
├── test/
│   ├── test_lab.py          # Automated tests
│   └── requirements.txt     # Test dependencies
└── README.md               # This file
```

## Quick Start

### Prerequisites
- Docker
- Python 3.11+
- Burp Suite Community Edition

### Installation
1. Clone the repository
2. Run `docker-compose up` to start the environment
3. Load the lab URL in Burp's browser: `http://localhost:3206`

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

## Issue Tracker

Report issues at: https://github.com/your-org/shoppingnow-lab/issues

---

*This is a deliberately vulnerable lab designed solely for educational purposes.* 