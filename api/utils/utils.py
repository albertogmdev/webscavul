import re
import unicodedata
    
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
    
def remove_accents(text: str) -> str:
    nfkd_form = unicodedata.normalize('NFKD', text)
    without_accents = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return without_accents

def format_json(obj):
    if isinstance(obj, dict):
        return {format_json(k): format_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [format_json(elem) for elem in obj]
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    else:
        return obj