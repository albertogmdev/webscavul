import requests
from requests.exceptions import RequestException

import app.utils.utils as utils

class Session:
    def __init__(self):
        self.domain = None
        self.full_domain = None
        self.schema = None
        self.response = None
        self.status = None
        self.error = None
        self.valid = True
    
    def set_domain(self, domain: str):
        if not domain:
            print("ERROR: URL del dominio obligatoria")
            return False
        if not utils.is_valid_domain(domain):
            print(f"ERROR: URL malformada o errónea - {domain}")
            return False
        
        if not domain.startswith(("http://", "https://")):
            self.domain = domain
        else:
            self.domain = domain.replace("http://", "").replace("https://", "")

        print(f"INFO: Dominio establecido a {self.domain}")
        return True

    def make_request(self):
        error = None
        schemas = ["https://", "http://"]

        for schema in schemas:
            full_domain = f"{schema}{self.domain}"
            try:
                response = requests.get(full_domain)
                status = response.status_code

                if status == 200:
                    self.schema = schema
                    self.status = status
                    self.full_domain = full_domain
                    self.response = response
                    print(f"INFO: Dominio {full_domain} accedido - status: {status}")
                    break
                else:
                    print(f"ERROR: Fallo al acceder a {full_domain} - status: {status}")
            except RequestException as e:
                print(f"ERROR: El dominio {full_domain} no resuelve o no es accesible")
                error = str(e)
        
        if not self.response:
            if error:
                self.error = error
            self.valid = False
            return False
        
        return True