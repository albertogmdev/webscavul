import requests
from requests.exceptions import RequestException

def analyze_tls(url: str) -> dict:
    try:
        print("hola")
    except RequestException as e:
        return {"error": str(e)}