import re
import requests
from requests.exceptions import RequestException
    
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
    
def remove_path(domain: str) -> str:
    if '/' in domain:
        return domain.split('/')[0]
    else:
        return domain