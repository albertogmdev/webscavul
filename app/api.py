from fastapi import FastAPI, Response, HTTPException

import app.utils.utils as utils
import app.modules.headers as headers
import app.modules.ssl as ssl
import app.modules.tls as tls
import app.modules.information as information
import app.modules.webparser as webparser
import app.modules.webanalyzer as webanalyzer

from app.core.webpage import WebPage
from app.core.session import Session

app = FastAPI()

@app.get("/test")
def test(domain: str):
    result = None
    session = Session()

    if session.set_domain(domain):
        if session.make_request():
            print(session.__dict__)
            result = session.response.headers
        else:
            raise HTTPException(status_code=400, detail=f"El dominio {session.domain} no resuelve o no es accesible")
    else:
        raise HTTPException(status_code=400, detail="Formato de dominio incorrecto o no válido")

    return result

@app.get("/custom-headers")
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
        with open('app/test/links.html', 'r', encoding='utf-8') as file:
            content += file.read()
        with open('app/test/script_tags.html', 'r', encoding='utf-8') as file:
            content += file.read()
        with open('app/test/link_tags.html', 'r', encoding='utf-8') as file:
            content += file.read()
        with open('app/test/metas.html', 'r', encoding='utf-8') as file:
            content += file.read()
    except FileNotFoundError:
        print("Error: El archivo no fue encontrado en la ruta especificada.")
        content = "<h1>Archivo no encontrado</h1>"
    except Exception as e:
        print(f"Ocurrió un error inesperado al leer el archivo: {e}")
        content = f"<h1>Error inesperado: {e}</h1>"
    content += "</body></html>"
    print(content)
    return Response(content=content, media_type="text/html", headers=headers)

@app.get("/analyze")
async def analyze(domain: str):
    session = Session()
    result = {}

    if session.set_domain(domain):
        if session.make_request():
            result_information = information.get_IP(session.full_domain, session.port)
            result_headers = headers.analyze_headers(session.response.headers)
            result_ssl = ssl.analyze_ssl(session.domain, session.schema)
            webpage = WebPage(session.domain)
            await webpage.load_webpage(session.full_domain)
            webparser.parse_webpage(webpage)
            result_syntax = webanalyzer.analyze_webpage(webpage, result_headers)

            result = {
                "information": result_information,
                "headers": result_headers,
                "ssl": result_ssl,
                "syntax": result_syntax
            }
        else:
            raise HTTPException(status_code=400, detail=f"El dominio {session.domain} no resuelve o no es accesible")
    else:
        raise HTTPException(status_code=400, detail="Formato de dominio incorrecto o no válido")
    
    return result

@app.get("/analyze/syntax")
async def analyze_syntax():
    result = {}
    headers = {"hsts":{"enabled":False},"csp":{"enabled":False},"xframe":{"enabled":False},"content_type":{"enabled":False,"correct":False},"cookie":{"enabled":False},"cache":{"enabled":False,"correct":False},"xss":{"enabled":False,"correct":False},"referrer":{"enabled":False,"correct":False},"permissions":{"enabled":False,"correct":False},"refresh":{"enabled":False}}

    webpage = WebPage("localhost/custom-headers")
    await webpage.load_webpage("http://localhost/custom-headers")
    webparser.parse_webpage(webpage)
    result['syntax'] = webanalyzer.analyze_webpage(webpage, headers)
    
    return result

@app.get("/analyze/tls")
def analyze_tls(domain: str):
    result = {}
    
    is_valid = utils.is_domain_valid(domain)
    if not is_valid["result"]:
        error = is_valid["error"] if hasattr(is_valid, "error") else is_valid["status_code"]
        raise HTTPException(status_code=400, detail=error)
    
    domain = is_valid["domain"]

    result = tls.analyze_tls(domain)

    return result

@app.get("/analyze/headers")
def analyze_headers(domain: str):
    result = {}
    
    is_valid = utils.is_domain_valid(domain)
    if not is_valid["result"]:
        error = is_valid["error"] if hasattr(is_valid, "error") else is_valid["status_code"]
        raise HTTPException(status_code=400, detail=error)
    
    domain = is_valid["domain"]

    result = headers.analyze_headers(domain)

    return result