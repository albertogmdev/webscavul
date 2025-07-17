import socket
from urllib.parse import urlparse

def get_IP(domain: str, port: int):
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = urlparse(domain).netloc
    if port:
        domain = domain.replace(f':{port}', '')
    return socket.gethostbyname_ex(domain)