import requests
from requests.exceptions import RequestException

def analyze_headers(url: str) -> dict:
    headers = {'user-agent': 'my-app/0.0.1'}
    if not url.startswith(("http://", "https://")):
        url = f"http://{url}"
    
    try:
        resp = requests.get(url, timeout=500, allow_redirects=True, headers=headers)
        return {
            "final_url": resp.url,
            "status_code": resp.status_code,
            "request_headers": dict(resp.request.headers),
            "response_headers": dict(resp.headers),
            "redirects": [
                {
                    "url": resp.url,
                    "status_code": resp.status_code,
                    "headers": dict(resp.headers)
                }
                for resp in resp.history
            ],
            "cookies": resp.cookies.get_dict()
        }
    except RequestException as e:
        # 2) Captura de errores de red (timeout, SSL, etc.)
        return {"error": str(e)}