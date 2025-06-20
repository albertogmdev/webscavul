import requests
from requests.exceptions import RequestException

def analyze_headers(url: str) -> dict: 
    try:
        response = requests.get(url)
        headers = response.headers
        
        hsts_info = check_hsts(headers)
        xframe_info = check_xframe(headers)
        content_info = check_content(headers)
        cookie_info = check_cookie(headers)
        csp_info = check_csp(headers)
        
        # Recomendables
        xss_info = check_xss(headers)
        referer_info = check_referer(headers)
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
            "referer": referer_info,
            "permissions": permission_info,
            "test": headers
        }
        
        return result
    except RequestException as e:
        return {"error": str(e)}

def check_hsts(headers: dict) -> dict:
    hsts = headers.get("strict-transport-security")
    
    if hsts:
        hsts_value = hsts.split("; ")
        return { "enabled": True, "correct": True, "value": hsts_value }
    else:
        return{ "enabled": False }
    
def check_content(headers: dict) -> dict:
    content = headers.get("x-content-type-options")
    if content:
        isCorrect = False
        
        if content.lower() == "nosniff": 
            isCorrect = True
        
        return {"enabled": True, "correct": isCorrect, "value": content}
    else:
        return {"enabled": False, "correct": False}

def check_xss(headers: dict) -> dict:
    xss = headers.get("x-xss-protection")
    
    if xss:
        isCorrect = False
        xss_value = xss.lower().split("; ")
        
        if "1" in xss_value and "mode=block" in xss_value:
            isCorrect = True
            
        return {"enabled": True, "correct": isCorrect, "value": xss}
    else:
        return {"enabled": False, "correct": False}

def check_xframe(headers: dict) -> dict:
    xframe = headers.get("x-frame-options")
    
    if xframe:
        isCorrect = False
        
        if xframe.lower() == "deny" or xframe.lower() == "sameorigin":
            isCorrect = True
            
        return {"enabled": True, "correct": isCorrect, "value": xframe}
    else:
        return {"enabled": False}

def check_permissions(headers: dict) -> dict:
    permission = headers.get("permissions-policy")
    
    if permission:
        permission_value = permission.lower().split(", ")

        return {"enabled": True, "correct": True, "value": permission_value}
    else:
        return {"enabled": False, "correct": False}

def check_referer(headers: dict) -> dict:
    referer = headers.get("referrer-policy")
    
    if referer:
        isCorrect = False
        referer_value = referer.lower().split(", ")
        
        if "no-referrer" in referer_value or "strict-origin-when-cross-origin" in referer_value:
            isCorrect = True
            
        return {"enabled": True, "correct": isCorrect, "value": referer_value}
    else:
        return {"enabled": False, "correct": False}

def check_cache(headers: dict) -> dict:
    cache = headers.get("cache-control")
    
    if cache:
        isCorrect = False
        cache_value = cache.lower().split(", ")
        
        if "no-store" in cache_value:
            isCorrect = True
            
        return {"enabled": True, "correct": isCorrect, "value": cache_value}
    else:
        return {"enabled": False, "correct": False}

def check_cookie(headers: dict) -> dict:
    cookie = headers.get("set-cookie")
    
    if cookie:
        cookie_value = cookie.lower().split("; ")
        isCorrect = False
        
        if "secure" in cookie_value and "httponly" in cookie_value:
            isCorrect = True
            
        return {"enabled": True, "correct": isCorrect, "value": cookie_value}
    else:
        return {"enabled": False}
    
def check_csp(headers: dict) -> dict:
    csp = headers.get("content-security-policy")
    
    if csp:
        csp_value = csp.split("; ")
        return {"enabled": True, "correct": True, "value": csp_value}
    else:
        return {"enabled": False}
