import os
import mysql.connector
import uuid
from hashlib import sha256

# DB config from environment
DB_CONFIG = {
    "host": os.environ.get("HOST", "localhost"),
    "user": os.environ.get("GG_USER", "root"),
    "password": os.environ.get("GG_PASS", ""),
    "database": os.environ.get("DB_NAME", "GrantGuruDB")
}

# Generate test user data
test_user = {
    "f_name": None,
    "m_name": None,
    "l_name": "User",
    "institution": "Some University",
    "email": f"test3@gmail.com",  # unique email
    "password": sha256("123456".encode()).hexdigest()     # hashed password
}

# Load SQL script and split into statements
with open("src/entity_crud_operations/users/create_users.sql", "r") as f:
    sql_script = f.read()

# Split by semicolon to get individual statements
statements = [s.strip() for s in sql_script.split(';') if s.strip()]

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Execute INSERT statement
    cursor.execute(statements[0], test_user)
    
    # Execute SELECT statement
    cursor.execute(statements[1], test_user)
    user_id = cursor.fetchone()[0]
    
    conn.commit()
    print(f"Inserted test user with user_id: {user_id}")
    
finally:
    cursor.close()
    conn.close()
