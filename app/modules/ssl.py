import requests
from requests.exceptions import RequestException

def analyze_ssl(url: str) -> dict:
    try:
        response = requests.get(url)
        
    except RequestException as e:
        return {"error": str(e)}