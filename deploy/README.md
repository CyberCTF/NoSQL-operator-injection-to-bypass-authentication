# ShoppingNow NoSQL Injection Lab

A deliberately vulnerable e-commerce application demonstrating MongoDB NoSQL injection vulnerabilities for educational purposes.

## Quick Start

### Pull the Image
```bash
docker pull cyberctf/nosql-injection-lab:latest
```

### Run the Container
```bash
docker run -d -p 3206:5000 --name nosql-lab cyberctf/nosql-injection-lab:latest
```

### Access the Application
Open your browser and navigate to: `http://localhost:3206`

## Demo Accounts

- **Customer:** john_doe / password123
- **Customer:** jane_smith / jane123
- **Admin:** admin / admin_secret_2024 (hidden account)

## Learning Objectives

- Identify NoSQL injection vectors in authentication endpoints
- Craft payloads using MongoDB operators ($ne and $regex)
- Bypass authentication to gain admin access

## Difficulty Level

**Beginner** - Estimated time: 20-30 minutes

## Prerequisites

- Basic web application penetration testing knowledge
- Familiarity with MongoDB query syntax
- Burp Suite or similar proxy tool

## Skills You'll Learn

- Finding and exploiting NoSQL injection vulnerabilities
- Crafting JSON injection payloads
- Authentication bypass strategies

## How to Report Issues

If you encounter any problems with this lab, please report them at:
https://github.com/cyberctf/nosql-injection-lab/issues

---

*This is a deliberately vulnerable lab designed solely for educational purposes.* 