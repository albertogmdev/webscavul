from fastapi import FastAPI, Response, HTTPException

import app.utils.utils as utils
import app.modules.headers as headers
import app.modules.ssl as ssl
import app.modules.tls as tls
import app.modules.information as information
import app.modules.webparser as webparser

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
    content = "<html><body><h1>Test Headers</h1></body></html>"
    return Response(content=content, media_type="text/html", headers=headers)

@app.get("/analyze")
async def analyze(domain: str):
    session = Session()
    result = {}

    if session.set_domain(domain):
        if session.make_request():

            result['information'] = information.get_IP(session.full_domain, session.port)
            result['headers'] = headers.analyze_headers(session.response.headers)
            result['ssl'] = ssl.analyze_ssl(session.domain, session.schema)

            webpage = WebPage()
            await webpage.load_webpage(session.full_domain)
            result['web'] = webparser.parse_webpage(webpage)
        else:
            raise HTTPException(status_code=400, detail=f"El dominio {session.domain} no resuelve o no es accesible")
    else:
        raise HTTPException(status_code=400, detail="Formato de dominio incorrecto o no válido")
    
    return result

@app.get("/analyze/ssl")
def analyze_ssl(domain: str):
    result = {}
    
    domain = is_valid["domain"]

    result = ssl.analyze_ssl(domain)

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

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}