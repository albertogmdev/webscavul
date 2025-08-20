import re

def analyze_headers(headers: dict) -> dict: 
    hsts_info = check_hsts(headers)
    xframe_info = check_xframe(headers)
    content_info = check_content(headers)
    cookie_info = check_cookie(headers)
    csp_info = check_csp(headers)
    
    # Recomendables
    xss_info = check_xss(headers)
    refesh_info = check_refesh(headers)
    referrer_info = check_referrer(headers)
    permission_info = check_permissions(headers)
    cache_info = check_cache(headers)
    
    result = {
        "hsts": hsts_info,
        "csp": csp_info,
        "xframe": xframe_info,
        "content_type": content_info,
        "cookie": cookie_info,
        "cache": cache_info,
        "xss": xss_info,
        "referrer": referrer_info,
        "permissions": permission_info,
        "refresh": refesh_info
    }
    
    return result

def check_hsts(headers: dict) -> dict:
    hsts = headers.get("strict-transport-security")
    result = {
        "severity": "warning", 
        "name": "Strict-Transport-Security", 
        "description": "Esta cabecera le dice al navegador que siempre debe conectarse al sitio usando HTTPS. Con ella se evita que alguien pueda obligar al usuario a usar HTTP, que es inseguro. Así, aunque el usuario escriba solo el dominio sin “https://”, el navegador recordará que siempre tiene que usar la versión segura. Es una forma de proteger las comunicaciones contra ataques que intentan interceptar o modificar la información.",
        "more": "https://developer.mozilla.org/es/docs/Web/HTTP/Headers/Strict-Transport-Security"
    }
    
    if hsts:
        hsts_value = re.split('; |, ', hsts.lower())

        result["value"] = hsts_value
        result["enabled"] = True
        result["correct"] = True
    else:
        result["enabled"] = False
        result["correct"] = False
    return result
    
def check_content(headers: dict) -> dict:
    content = headers.get("x-content-type-options")
    result = {
        "severity": "warning", 
        "name": "Content-Type-Options", 
        "description": "Sirve para indicar al navegador que no intente adivinar el tipo de contenido de un archivo. Sin esta cabecera, a veces el navegador intenta “interpretar” un archivo y puede abrirlo de forma peligrosa. Con la opción nosniff, se asegura de que solo se use el tipo correcto. Esto evita que se ejecuten archivos como si fueran código cuando en realidad no deberían serlo, reduciendo riesgos de ataques.",
        "recommendation": "nosniff",
        "more": "https://developer.mozilla.org/es/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options"
    }

    if content:
        isCorrect = False
        
        if content.lower() == "nosniff": 
            isCorrect = True
        
        result["value"] = content
        result["enabled"] = True
        result["correct"] = isCorrect
    else:
        result["enabled"] = False
        result["correct"] = False
    
    return result

def check_xss(headers: dict) -> dict:
    xss = headers.get("x-xss-protection")
    result = {
        "severity": "recommendation", 
        "name": "X-XSS-Protection", 
        "description": "Es una protección adicional contra ataques de Cross-Site Scripting (XSS). Indica al navegador que bloquee páginas si detecta que se intenta inyectar código malicioso. Aunque hoy en día los navegadores modernos ya tienen protecciones integradas y se recomienda usar otras cabeceras más completas, esta todavía puede ser útil como capa extra para mejorar la seguridad en navegadores más antiguos.",
        "recommendation": "1; mode=block",
        "more": "https://developer.mozilla.org/es/docs/Web/HTTP/Headers/X-XSS-Protection"
    }
    
    if xss:
        isCorrect = False
        xss_value = re.split('; |, ', xss.lower())
        
        if "1" in xss_value and "mode=block" in xss_value:
            isCorrect = True
            
        result["value"] = xss_value
        result["enabled"] = True
        result["correct"] = isCorrect
    else:
        result["enabled"] = False
        result["correct"] = False
    
    return result

def check_xframe(headers: dict) -> dict:
    xframe = headers.get("x-frame-options")
    result = {
        "severity": "recommendation", 
        "name": "X-Frame-Options", 
        "description": "Controla si una página puede ser embebida dentro de un iframe en otros sitios web. Esto previene ataques de clickjacking, en los que un atacante engaña al usuario para hacer click en un botón o enlace oculto dentro de un frame malicioso. Sus valores más seguros son DENY (bloquea completamente el embebido) y SAMEORIGIN (solo permite si el origen es el mismo). Aunque está en desuso en favor de CSP (frame-ancestors), sigue siendo muy utilizada.",
        "recommendation": "DENY o SAMEORIGIN",
        "more": "https://developer.mozilla.org/es/docs/Web/HTTP/Headers/X-Frame-Options"
    }
    
    if xframe:
        isCorrect = False
        
        if xframe.lower() == "deny" or xframe.lower() == "sameorigin":
            isCorrect = True
            
        result["value"] = xframe
        result["enabled"] = True
        result["correct"] = isCorrect
    else:
        result["enabled"] = False
        result["correct"] = False

    return result
    
def check_refesh(headers: dict) -> dict:
    refresh = headers.get("refresh")
    result = {
        "severity": "recommendation", 
        "name": "Refresh", 
        "description": "Esta cabecera le dice al navegador que recargue o redirija a otra página después de un tiempo. Aunque no es peligrosa en sí, puede ser usada por atacantes para redirigir a usuarios a webs falsas sin que se den cuenta. Por eso se recomienda evitar su uso y en su lugar manejar redirecciones desde el servidor de forma más controlada.",
        "recommendation": "Evitar su uso",
        "more": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Refresh"
    }
    
    if not refresh:
        result["enabled"] = False
        result["correct"] = True
    else:
        result["enabled"] = True
        result["correct"] = False
        result["value"] = refresh

    return result  

def check_permissions(headers: dict) -> dict:
    permission = headers.get("permissions-policy")
    result = {
        "severity": "recommendation", 
        "name": "Permissions-Policy", 
        "description": "Permite controlar qué funciones del navegador puede usar la página. Por ejemplo, se puede decidir si el sitio puede acceder a la cámara, micrófono o ubicación. Esto protege al usuario, porque sin restricciones un sitio malicioso podría abusar de esos permisos. Es una forma de dar a la aplicación solo los accesos estrictamente necesarios, aumentando la privacidad y seguridad.",
        "more": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy"
    }
    
    if permission:
        permission_value = re.split('; |, ', permission.lower())

        result["value"] = permission_value
        result["enabled"] = True
        result["correct"] = True
    else:
        result["enabled"] = False
        result["correct"] = False

    return result

def check_referrer(headers: dict) -> dict:
    referrer = headers.get("referrer-policy")
    result = {
        "severity": "recommendation", 
        "name": "Referrer-Policy", 
        "description": "Indica qué información se envía a otros sitios cuando el usuario hace clic en un enlace. Sin esta cabecera, el navegador puede mandar la dirección completa de la página, incluyendo datos sensibles. Configurando la política, se puede limitar la información compartida, protegiendo la privacidad del usuario y reduciendo el riesgo de que datos importantes se filtren a páginas externas.",
        "recommendation": "no-referrer, strict-origin-when-cross-origin, no-referrer-when-downgrade, strict-origin",
        "more": "https://developer.mozilla.org/es/docs/Web/HTTP/Headers/Referrer-Policy"
    }
    
    if referrer:
        isCorrect = False
        
        if referrer not in ['no-referrer', 'strict-origin-when-cross-origin', 'no-referrer-when-downgrade', 'strict-origin']:
            isCorrect = True
            
        result["value"] = referrer
        result["enabled"] = True
        result["correct"] = isCorrect
    else:
        result["enabled"] = False
        result["correct"] = False
    
    return result

def check_cache(headers: dict) -> dict:
    cache = headers.get("cache-control")
    result = {
        "severity": "warning", 
        "name": "Cache-Control", 
        "description": "Sirve para controlar cómo se guardan copias de la página en caché. Si no se configura bien, un navegador o proxy podría almacenar datos sensibles (como información de usuario o páginas privadas) y mostrarlos después a otra persona. Con valores como no-store, se evita que información importante se quede guardada en la memoria del navegador. También ayuda a definir políticas de rendimiento en recursos estáticos cuando se ajusta con max-age o public.",
        "recommendation": "no-store, no-cache, private, public",
        "more": "https://developer.mozilla.org/es/docs/Web/HTTP/Headers/Cache-Control"
    }
    
    if cache:
        isCorrect = False
        cache_value = re.split('; |, ', cache.lower())
        
        if "no-store" in cache_value:
            isCorrect = True
        
        result["value"] = cache_value
        result["enabled"] = True
        result["correct"] = isCorrect
    else:
        result["enabled"] = False
        result["correct"] = False

    return result

def check_cookie(headers: dict) -> dict:
    cookie = headers.get("set-cookie")
    result = {
        "severity": "warning", 
        "name": "Set-Cookie", 
        "description": "Permite configurar cookies seguras en el navegador. Las banderas Secure aseguran que solo viajen por HTTPS, mientras que HttpOnly evita que sean accesibles desde JavaScript, reduciendo riesgos de robo mediante XSS. Su correcta configuración es esencial en la protección de sesiones de usuario y autenticación. Una cookie sin estas opciones puede ser interceptada o manipulada, abriendo la puerta a secuestro de sesión (session hijacking).",
        "recommendation": "Secure; HttpOnly",
        "more": "https://developer.mozilla.org/es/docs/Web/HTTP/Headers/Set-Cookie"
    }
    
    if cookie:
        cookie_value = re.split('; |, ', cookie.lower())
        isCorrect = False
        
        if "secure" in cookie_value and "httponly" in cookie_value:
            isCorrect = True

        result["value"] = cookie_value
        result["enabled"] = True
        result["correct"] = isCorrect
    else:
        result["enabled"] = False
        result["correct"] = False

    return result
    
def check_csp(headers: dict) -> dict:
    csp = headers.get("content-security-policy")
    result = {
        "severity": "critical",
        "name": "Content-Security-Policy",
        "description": "Es una de las cabeceras más importantes porque permite definir qué contenido puede cargarse en la página (scripts, imágenes, estilos, etc.). Con ella se evita que se ejecute código que no venga de fuentes de confianza, protegiendo contra ataques como la inyección de scripts (XSS). Bien configurada, actúa como una 'lista blanca' de lo que el navegador puede mostrar o ejecutar.",
        "more": "https://developer.mozilla.org/es/docs/Web/HTTP/CSP"
    }
    
    if csp:
        csp_value = re.split('; |, ', csp.lower())

        result["value"] = csp_value
        result["enabled"] = True
        result["correct"] = True
    else:
        result["enabled"] = False
        result["correct"] = False

    return result
