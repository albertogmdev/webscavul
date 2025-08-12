from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.webpage import WebPage
from core.session import Session
from core.models import ListCreate, ListUpdate, TaskCreate, TaskUpdate

import utils.utils as utils
import utils.database as database
import modules.headers as headers
import modules.ssl as ssl
import modules.information as information
import modules.webparser as webparser
import modules.webanalyzer as webanalyzer

api = FastAPI()
origins = ["http://localhost", "http://localhost:3000"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,     
    allow_methods=["*"],  
    allow_headers=["*"],
)
db_connection = None

@api.on_event("startup")
def startup_event():
    print("INFO: Intializing db connection")
    global db_connection
    db_connection = database.create_db_connection()

    ## Usage of connection pool
    # pool = database.create_db_pool(5)
    # connection = pool.get_connection()
    # cur = conn.cursor()
    # Execute actions in DB
    # cur.close()
    # conn.close()

@api.on_event("shutdown")
def shutdown_event():
    global db_connection
    if db_connection:
        db_connection.close()

@api.get("/custom-headers")
def custom_headers():
    headers = {
        "Strict-Transport-Security": "max-age=63072000; includeSubDomains; preload",
        "Content-Security-Policy": "default-src 'self'",
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "no-referrer",
        "Permissions-Policy": "geolocation=()",
        "Cache-Control": "no-store",
        "X-XSS-Protection": "1; mode=block",
        "Set-Cookie": "sessionid=12345; Secure; HttpOnly; SameSite=Strict"
    }

    content = "<!DOCTYPE html><html lang='en'><head><title>Document</title></head><body>"
    
    try:
        with open('api/test/links.html', 'r', encoding='utf-8') as file:
            content += file.read()
        with open('api/test/script_tags.html', 'r', encoding='utf-8') as file:
            content += file.read()
        with open('api/test/link_tags.html', 'r', encoding='utf-8') as file:
            content += file.read()
        with open('api/test/metas.html', 'r', encoding='utf-8') as file:
            content += file.read()
        with open('api/test/forms.html', 'r', encoding='utf-8') as file:
            content += file.read()
    except FileNotFoundError:
        print("Error: El archivo no fue encontrado en la ruta especificada.")
        content = "<h1>Archivo no encontrado</h1>"
    except Exception as e:
        print(f"Ocurrió un error inesperado al leer el archivo: {e}")
        content = f"<h1>Error inesperado: {e}</h1>"
    content += "</body></html>"
    
    return Response(content=content, media_type="text/html", headers=headers)

@api.get("/analyze")
async def analyze(domain: str):
    session = Session()

    if session.set_domain(domain):
        if session.make_request():
            result_information = information.get_IP(session.full_domain, session.port)
            result_headers = headers.analyze_headers(session.response.headers)
            result_ssl = ssl.analyze_ssl(session.domain, session.schema)
            
            webpage = WebPage(session.domain)
            await webpage.load_webpage(session.full_domain)
            webparser.parse_webpage(webpage)
            webanalyzer.analyze_webpage(webpage, result_headers)
            
            response = database.create_report(db_connection, session, result_information, result_headers, result_ssl, webpage.vulnerabilities)
            if response["status"] != 200:
                raise HTTPException(
                    status_code=500,
                    detail={
                        "status": "error",
                        "message": f"Error al crear el informe para el dominio {domain}"
                    }
                )
            else:
                return {
                    "status": "success", 
                    "message": f"Informe creado con éxito.",
                    "data": response["data"]
                }
        else:
            raise HTTPException(status_code=400, detail=f"El dominio {session.domain} no resuelve o no es accesible")
    else:
        raise HTTPException(status_code=400, detail="Formato de dominio incorrecto o no válido")

@api.get("/analyze/syntax")
async def analyze_syntax():
    result = {}
    headers = {"hsts":{"enabled":False},"csp":{"enabled":False},"xframe":{"enabled":False},"content_type":{"enabled":False,"correct":False},"cookie":{"enabled":False},"cache":{"enabled":False,"correct":False},"xss":{"enabled":False,"correct":False},"referrer":{"enabled":False,"correct":False},"permissions":{"enabled":False,"correct":False},"refresh":{"enabled":False}}

    webpage = WebPage("localhost/custom-headers")
    await webpage.load_webpage("http://localhost/custom-headers")
    webparser.parse_webpage(webpage)
    result['syntax'] = webanalyzer.analyze_webpage(webpage, headers)
    
    return result

# Database operations endpoints
## REPORT
@api.get("/report/{report_id}")
def get_report(report_id: str):
    report = database.get_report_by_id(db_connection, report_id)
    if not report:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Informe {report_id} no encontrado."
            }
        )

    return {
        "status": "success", 
        "message": f"Informe {report_id} encontrado.",
        "data": {"report": report}
    }

@api.get("/report/{report_id}/board")
def get_report_board(report_id: str):
    if not database.get_report_by_id(db_connection, report_id):
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Reporte {report_id} no encontrado."
            }
        )

    board = database.get_report_board(db_connection, report_id)
    if not board:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Tablero del informe {report_id} no encontrado o no se encontraron listas de tareas."
            }
        )

    return {
        "status": "success", 
        "message": f"Informe {report_id} encontrado.",
        "data": {"board": board}
    }

@api.delete("/report/{report_id}")
def delete_report(report_id: str):
    if not database.get_report_by_id(db_connection, report_id):
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Informe {report_id} no encontrado."
            }
        )

    deleted = database.delete_report(db_connection, report_id)
    if not deleted:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Error al eliminar el informe {report_id}"
            }
        )

    return {
        "status": "success", 
        "message": f"Informe {report_id} eliminado correctamente",
        "data": {"report_id": report_id}
    }

## LIST
@api.get("/list/{list_id}")
def get_list(list_id: str):
    list = database.get_list_by_id(db_connection, list_id)
    if not list: 
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Lista {list_id} no encontrada."
            }
        )

    return {
        "status": "success", 
        "message": f"Lista {list_id} encontrada.",
        "data": {"list": list}
    }

@api.get("/report/{report_id}/lists")
def get_report_lists(report_id: str):
    if not database.get_report_by_id(db_connection, report_id): 
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Informe {report_id} no encontrado."
            }
        )

    lists = database.get_lists_by_report(db_connection, report_id)
    if not lists: 
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Listas del reporte {report_id} no encontradas."
            }
        )

    return {
        "status": "success", 
        "message": f"Listas de del reporte {report_id} encontradas.",
        "data": {"lists": lists}
    }

@api.post("/list")
def create_list(list: ListCreate):
    list_id = database.create_list(db_connection, list)
    if not list_id:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Error al crear la lista {list.title}"
            }
        )

    return {
        "status": "success", 
        "message": f"Lista {list_id} creada correctamente.",
        "data": {"list_id": list_id}
    }

@api.delete("/list/{list_id}")
def delete_list(list_id: str):
    deleted = database.delete_list(db_connection, list_id)
    if not deleted:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Error al eliminar la lista {list_id}."
            }
        )

    return {
        "status": "success", 
        "message": f"Lista {list_id} eliminada correctamente.",
        "data": {"list_id": list_id}
    }

@api.put("/list/{list_id}")
def update_list(list_id: str, list: ListUpdate):
    update_fields = {key: value for key, value in list.dict().items() if value is not None}
    if not update_fields or len(update_fields) <= 1:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": "No se proporcionaron campos válidos a actualizar."
            }
        )

    new_list = database.update_list(db_connection, list_id, update_fields)
    if not new_list:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Error al actualizar la lista {list_id} o el 'report_id' es incorrecto."
            }
        )

    return {
        "status": "success", 
        "message": f"Lista {list_id} actualizada correctamente.",
        "data": {"list": new_list}
    }

## TASK
@api.get("/task/{task_id}")
def get_task(task_id: str):
    task = database.get_task_by_id(db_connection, task_id)
    if not task: 
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Tarea {task_id} no encontrada."
            }
        )

    return {
        "status": "success", 
        "message": f"Tarea {task_id} encontrada.",
        "data": {"task": task}
    }

@api.get("/list/{list_id}/tasks")
def get_list_tasks(list_id: str):
    if not database.get_list_by_id(db_connection, list_id): 
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Lista {list_id} no encontrada."
            }
        )

    tasks = database.get_tasks_by_list(db_connection, list_id)
    if not tasks: 
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": f"Tareas de las lista {list_id} no encontradas."
            }
        )

    return {
        "status": "success", 
        "message": f"Tareas de las lista {list_id} encontradas.",
        "data": {"tasks": tasks}
    }

@api.post("/task")
def create_task(task: TaskCreate):
    task_id = database.create_task(db_connection, task)
    if not task_id:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Error al crear la lista {task.title}"
            }
        )

    return {
        "status": "success", 
        "message": f"Tarea '{task.title}' creada correctamente.",
        "data": {"task_id": task_id}
    }

@api.delete("/task/{task_id}")
def delete_task(task_id: str):
    deleted = database.delete_task(db_connection, task_id)
    if not deleted:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Error al eliminar la tarea {task_id}."
            }
        )

    return {
        "status": "success", 
        "message": f"Tarea {task_id} eliminada correctamente.",
        "data": {"task_id": task_id}
    }

@api.put("/task/{task_id}")
def update_task(task_id: str, task: TaskUpdate):
    update_fields = {key: value for key, value in task.dict().items() if value is not None}
    if not update_fields or len(update_fields) < 1:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": "No se proporcionaron campos válidos a actualizar."
            }
        )

    new_task = database.update_task(db_connection, task_id, update_fields)
    if not new_task:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Error al actualizar la tarea {task_id} o el 'list_id' es incorrecto."
            }
        )

    return {
        "status": "success", 
        "message": f"Tarea {task_id} actualizada correctamente.",
        "data": {"task": new_task}
    }