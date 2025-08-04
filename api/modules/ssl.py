import socket
import ssl
import OpenSSL
import api.utils.utils as utils

from datetime import datetime

def analyze_ssl(domain: str, schema: str) -> dict:
    if schema == "http":
        return {"error": "not_supported", "message": "SSL/TLS no es compatible con HTTP"}

    domain = utils.remove_path(domain)
    context = ssl.create_default_context()
    certificate = get_certificate(context, domain)
    tls = get_tls_info(context, domain)
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)

    result = {
        'subject': dict(x509.get_subject().get_components()),
        'issuer': dict(x509.get_issuer().get_components()),
        'serial_number': x509.get_serial_number(),
        'version': x509.get_version(),
        'not_before': datetime.strptime(x509.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ'),
        'not_after': datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ'),
        'tls_version': tls['version'],
        'tls_cipher': tls['cipher'],
    }

    return result

def get_certificate(context, host, port=443, timeout=10):
    conn = socket.create_connection((host, port))
    sock = context.wrap_socket(conn, server_hostname=host)
    sock.settimeout(timeout)

    try:
        der_cert = sock.getpeercert(True)
    finally:
        sock.close()

    return ssl.DER_cert_to_PEM_cert(der_cert)

def get_tls_info(context, host, port=443):
    version = None
    cipher = None

    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            version = ssock.version()
            cipher = ssock.cipher()
    
    if cipher: cipher = cipher[0]

    return { "version": version, "cipher": cipher }