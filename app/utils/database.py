import mariadb
import os
import sys
import json
import time
import hashlib
import datetime

from mariadb import ConnectionPool
from dotenv import load_dotenv

# Create a db connection pool
def create_db_pool(threads: int) -> ConnectionPool:
    load_dotenv()
    try:
        pool = ConnectionPool(
            pool_name="mypool",
            pool_size=threads,
            user=os.environ['DB_ROOT_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=int(os.environ['DB_PORT']),
            database=os.environ['DB_NAME']
        )
    except mariadb.Error as e:
        print(f"Error creating DB pool connection: {e}")
        sys.exit(1)
    
    return pool

# Create a single db connection
def create_db_connection():
    load_dotenv()
    connection = None

    for connection_try in range(10):
        try:
            connection = mariadb.connect(
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD'],
                host=os.environ['DB_HOST'],
                port=int(os.environ['DB_PORT']),
                database=os.environ['DB_NAME']
            )

            print("INFO: Connected to MariaDB!")
            return connection
        except mariadb.Error as e:
            print(f"INFO: Try {connection_try+1}/10, {e}")
            time.sleep(3)

    print("ERROR: Imposible to connect, several tries done.")
    sys.exit(1)
    
    return connection

def create_report(db_connection, session, information, headers, ssl) -> dict:
    try: 
        cursor = db_connection.cursor()
        report_id = hashlib.sha256(f"{session.full_domain}{datetime.datetime.now()}".encode()).hexdigest()
        report_title = f"Informe para {session.full_domain}"
        report_port = session.port if session.port else 0

        sql = "INSERT INTO Report \
            (id, title, domain, full_domain, protocol, ip, port, hsts, csp, xframe, content_type, cookie, cache, xss, referrer, permissions, refresh) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = (report_id, report_title , session.domain, session.full_domain, session.schema, json.dumps(information), report_port, json.dumps(headers['hsts']), json.dumps(headers['csp']), json.dumps(headers['xframe']), json.dumps(headers['content_type']), json.dumps(headers['cookie']), json.dumps(headers['cache']), json.dumps(headers['xss']), json.dumps(headers['referrer']), json.dumps(headers['permissions']), json.dumps(headers['refresh']))
        cursor.execute(sql, data)

        db_connection.commit()
        cursor.close()
    except mariadb.Error as e:
        db_connection.rollback()
        return {"status": 500, "error": e}
    
    return {"status": "ok", "report_id": report_id}