import mariadb
import os
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=os.environ['HOME'],
        password=os.environ['HOME'],
        host="192.0.2.1",
        port=3306,
        database="employees"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()