"""
Test MySQL Connection Script

This script helps you test different MySQL passwords to find the correct one.
"""

import mysql.connector
from mysql.connector import Error

def test_connection(password):
    """Test MySQL connection with a given password."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✓ SUCCESS! Connected to MySQL Server version {db_info}")
            print(f"✓ Password that works: '{password}'")
            connection.close()
            return True
    except Error as e:
        print(f"✗ Failed with password '{password}': {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("MySQL Connection Tester")
    print("=" * 60)
    print()

    # Test common passwords
    passwords_to_test = [
        "Kappa20205!",
        "Kappa20205",
        "",  # Empty password
        "root",
        "password",
        "mysql",
        "admin"
    ]

    print("Testing common passwords...")
    print()

    for pwd in passwords_to_test:
        display_pwd = pwd if pwd else "(empty/blank)"
        print(f"Testing: {display_pwd}")
        if test_connection(pwd):
            print()
            print("=" * 60)
            print(f"FOUND IT! Your MySQL password is: '{pwd}'")
            print(f"Update your .env file with: GG_PASS={pwd}")
            print("=" * 60)
            break
        print()
    else:
        print("=" * 60)
        print("None of the common passwords worked.")
        print()
        print("Please try entering your password manually:")
        print("1. You may need to reset your MySQL root password")
        print("2. Or check your MySQL installation documentation")
        print("=" * 60)

    input("\nPress Enter to exit...")
