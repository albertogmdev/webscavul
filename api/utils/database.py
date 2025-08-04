import mariadb
import os
import sys
import json
import time
import hashlib
import datetime

from mariadb import ConnectionPool
from dotenv import load_dotenv
from api.core.models import ListCreate, ListUpdate, TaskCreate, TaskUpdate

report_fields = ["id", "title", "created_at", "domain", "full_domain", "protocol", "ip", "port", "hsts", "csp", "xframe", "content_type", "cookie", "cache", "xss", "referrer", "permissions", "refresh"]
report_json_fields = ["hsts", "csp", "xframe", "content_type", "cookie", "cache", "xss", "referrer", "permissions", "refresh"]

list_fields = ["id", "report_id", "title"]

task_fields = ["id", "list_id", "title", "type", "severity", "location", "details", "status", "archived"]

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

# REPORT CRUD
def create_report(db_connection, session, information, headers, ssl, vulnerabilities) -> dict:
    try: 
        cursor = db_connection.cursor()
        report_id = hashlib.sha256(f"{session.full_domain}{datetime.datetime.now()}".encode()).hexdigest()
        report_title = f"Informe para {session.full_domain}"
        report_port = session.port if session.port else 0

        # Insert report info
        report_sql = "INSERT INTO Report \
            (id, title, domain, full_domain, protocol, ip, port, hsts, csp, xframe, content_type, cookie, cache, xss, referrer, permissions, refresh) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        report_data = (report_id, report_title , session.domain, session.full_domain, session.schema, json.dumps(information), report_port, json.dumps(headers['hsts']), json.dumps(headers['csp']), json.dumps(headers['xframe']), json.dumps(headers['content_type']), json.dumps(headers['cookie']), json.dumps(headers['cache']), json.dumps(headers['xss']), json.dumps(headers['referrer']), json.dumps(headers['permissions']), json.dumps(headers['refresh']))
        cursor.execute(report_sql, report_data)

        # Create default list
        list_sql = "INSERT INTO List \
            (report_id, title, archived) \
            VALUES (?, ?, 0) RETURNING id"
        list_data = (report_id, "TAREAS")
        cursor.execute(list_sql, list_data)
        result_list = cursor.fetchone()
        list_id = result_list[0]

        # Create al tasks
        tasks_sql = "INSERT INTO Task \
            (list_id, title, type, severity, location, details, status, archived) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        tasks_data = []
        for vulnerability in vulnerabilities:
            tasks_data.append((
                list_id,
                vulnerability.name,
                vulnerability.type,
                vulnerability.severity,
                vulnerability.location,
                vulnerability.details,
                0,
                False,
            ))
        cursor.executemany(tasks_sql, tasks_data)

        db_connection.commit()
        cursor.close()
    except mariadb.Error as e:
        db_connection.rollback()
        return {"status": 500, "error": e}
    except Exception as e:
        db_connection.rollback()
        return {"status": 500, "error": e}
    
    return {"status": "ok", "data": {"report_id": report_id}}

def get_report_by_id(db_connection, report_id):
    try: 
        cursor = db_connection.cursor()
        
        sql = "SELECT * FROM Report WHERE id = ?"
        data = (report_id,)
        cursor.execute(sql, data)
        row = cursor.fetchone()
        report = dict(zip(report_fields, row)) if row else None

        if report: 
            for json_field in report_json_fields:
                value = report.get(json_field)
                if value and isinstance(value, str):
                    try: report[json_field] = json.loads(value)
                    except json.JSONDecodeError: pass

        cursor.close()
        return report
    except Exception as e:
        return None

def get_report_board(db_connection, report_id):
    board = []
    try:
        cursor = db_connection.cursor()

        sql = "SELECT * FROM List WHERE report_id = ?"
        data = (report_id,)
        cursor.execute(sql, data)
        lists = cursor.fetchall()

        for item_list in lists:
            task_list = []
            list = dict(zip(list_fields, item_list))
            list_id = list.get("id")

            tasks_sql = "SELECT * FROM Task WHERE list_id = ?"
            tasks_data = (list_id,)
            cursor.execute(tasks_sql, tasks_data)
            tasks = cursor.fetchall()

            for item_task in tasks:
                task = dict(zip(task_fields, item_task))
                task_list.append(task)

            list["tasks"] = task_list
            board.append(list)
        
        cursor.close()
        return board if len(board) > 0 else None
    except Exception as e:
        return None
        
def delete_report(db_connection, report_id):
    try: 
        cursor = db_connection.cursor()

        sql = "DELETE FROM Report WHERE id = ?"
        data = (report_id,)
        cursor.execute(sql, data)
        db_connection.commit()
        deleted = cursor.rowcount > 0

        cursor.close()
        return deleted
    except Exception as e:
        return False

# List CRUD
def get_list_by_id(db_connection, list_id: str):
    try: 
        cursor = db_connection.cursor()

        sql = "SELECT * FROM List WHERE id = ?"
        data = (list_id,)
        cursor.execute(sql, data)
        row = cursor.fetchone()

        cursor.close()
        return dict(zip(list_fields, row)) if row else None
    except Exception as e:
        return False

def get_lists_by_report(db_connection, report_id: str):
    list_list = []
    try: 
        cursor = db_connection.cursor()

        sql = "SELECT * FROM List WHERE report_id = ?"
        data = (report_id,)
        cursor.execute(sql, data)
        lists = cursor.fetchall()

        for item_list in lists:
            list = dict(zip(list_fields, item_list))
            list_list.append(list)

        cursor.close()
        return list_list if len(list_list) > 0 else None
    except Exception as e:
        return False

def create_list(db_connection, list: ListCreate):
    try: 
        cursor = db_connection.cursor()

        sql = "INSERT INTO List \
            (report_id, title) \
            VALUES (?, ?) RETURNING id"
        data = (list.report_id, list.title)
        cursor.execute(sql, data)
        result_list = cursor.fetchone()

        cursor.close()
        return result_list[0] if result_list else None
    except Exception as e:
        return False

def delete_list(db_connection, list_id: str):
    try: 
        cursor = db_connection.cursor()

        sql = "DELETE FROM List WHERE id = ?"
        data = (list_id,)
        cursor.execute(sql, data)
        db_connection.commit()
        deleted = cursor.rowcount > 0

        cursor.close()
        return deleted
    except Exception as e:
        return False

def update_list(db_connection, list_id: str, fields: dict):
    try: 
        cursor = db_connection.cursor()

        columns = ", ".join([f"{key} = ?" for key in fields.keys()])
        sql = f"UPDATE List SET {columns} WHERE id = ?"
        data = list(fields.values()) + [list_id]
        cursor.execute(sql, data)
        db_connection.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            return None
        
        # Get updated list new data
        result_sql = "SELECT * FROM List WHERE id = ?"
        result_data = (list_id,)
        cursor.execute(result_sql, result_data)
        row = cursor.fetchone()

        cursor.close()
        return dict(zip(list_fields, row)) if row else None
    except Exception as e:
        db_connection.rollback()
        return False

# Task CRUD
def get_task_by_id(db_connection, task_id: str):
    try: 
        cursor = db_connection.cursor()

        sql = "SELECT * FROM Task WHERE id = ?"
        data = (task_id,)
        cursor.execute(sql, data)
        row = cursor.fetchone()

        cursor.close()
        return dict(zip(task_fields, row)) if row else None
    except Exception as e:
        return False

def get_tasks_by_list(db_connection, list_id: str):
    task_list = []
    try: 
        cursor = db_connection.cursor()

        sql = "SELECT * FROM Task WHERE list_id = ?"
        data = (list_id,)
        cursor.execute(sql, data)
        tasks = cursor.fetchall()

        for item_task in tasks:
            task = dict(zip(task_fields, item_task))
            task_list.append(task)

        return task_list if len(task_list) > 0 else None
    except Exception as e:
        return False

def create_task(db_connection, task: TaskCreate):
    try: 
        cursor = db_connection.cursor()

        sql = "INSERT INTO Task \
            (list_id, title, type, severity, location, details, status, archived) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING id"
        task_location = task.location if task.location else ""
        task_details = task.details if task.details else ""
        data = (task.list_id, task.title, task.type, task.severity, task_location, task_details, task.status, task.archived)
        cursor.execute(sql, data)
        result_task = cursor.fetchone()

        cursor.close()
        return result_task[0] if result_task else None
    except Exception as e:
        return False

def delete_task(db_connection, task_id: str):
    try: 
        cursor = db_connection.cursor()

        sql = "DELETE FROM Task WHERE id = ?"
        data = (task_id,)
        cursor.execute(sql, data)
        db_connection.commit()
        deleted = cursor.rowcount > 0

        cursor.close()
        return deleted
    except Exception as e:
        return False

def update_task(db_connection, task_id: str, fields: dict):
    try: 
        cursor = db_connection.cursor()

        columns = ", ".join([f"{key} = ?" for key in fields.keys()])
        sql = f"UPDATE Task SET {columns} WHERE id = ?"
        data = list(fields.values()) + [task_id]
        cursor.execute(sql, data)
        db_connection.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            return None
        
        # Get updated list new data
        result_sql = "SELECT * FROM Task WHERE id = ?"
        result_data = (task_id,)
        cursor.execute(result_sql, result_data)
        row = cursor.fetchone()

        cursor.close()
        return dict(zip(task_fields, row)) if row else None
    except Exception as e:
        db_connection.rollback()
        return False