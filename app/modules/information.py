import socket
from urllib.parse import urlparse

def get_IP(domain: str):
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = urlparse(domain).netloc
    return socket.gethostbyname_ex(domain)