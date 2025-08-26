import socket
from urllib.parse import urlparse

def get_information(domain, port, headers):
    socket = get_socket(domain, port)
    server_info = get_server(headers)
    ip_info = list(set(socket[2])) if socket[2] else None
    alias_info = socket[1] if socket[1] else None

    return {
        "ip": ip_info,
        "alias": alias_info,
        "server": server_info["server"],
        "powered": server_info["powered_by"],
        "generator": server_info["generator"]
    }

def get_socket(domain: str, port: int):
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = urlparse(domain).netloc
    if port:
        domain = domain.replace(f':{port}', '')

    # This function returns a tuple (hostname, aliaslist, ipaddrlist)
    return socket.gethostbyname_ex(domain)

def get_server(headers):
    server = headers.get("Server")
    powered_by = headers.get("X-Powered-By")
    generator = headers.get("X-Generator")

    return {
        "server": server,
        "powered_by": powered_by,
        "generator": generator
    }