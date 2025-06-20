import requests
from requests.exceptions import RequestException

def is_domain_valid(domain: str) -> bool:
    """
    Check if a domain given is valid, return a 200 code, or not.
    """
    
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