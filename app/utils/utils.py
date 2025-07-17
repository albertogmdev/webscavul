import re
import requests
from requests.exceptions import RequestException

def is_domain_valid(domain: str) -> bool:
    try:
        if not domain:
            print("ERROR: URL del dominio obligatoria")
            return {"result": False, "error": "La URL del dominio es obligatoria"}

        if not domain.startswith(("http://", "https://")):
            domain = f"http://{domain}"
            
        response = requests.get(domain)
        status = response.status_code
        print(f"INFO: Dominio {domain} accedido con status {status}")
        
        return {"result": status == 200, "status_code": response.status_code, "domain": domain}
    except RequestException:
        print(f"ERROR: El dominio {domain} no resuelve o no es accesible")
        return {"result": False, "error": "El dominio no resuelve o no es accesible"}
    
def is_valid_domain(domain: str) -> bool:
    regex = re.compile(
        r'^(?:https?://)?'                     
        r'(?:localhost(?:\:\d+)?'              
        r'|(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,})' 
        r'(?:\:\d+)?'                  
        r'(?:/.*)?$' , re.IGNORECASE
    )

    return domain is not None and regex.search(domain)

def get_port(domain: str) -> int:
    port = re.search(r':(\d+)', domain)
    print(print)
    if port:    
        return int(port.group(1))
    else:
        return None