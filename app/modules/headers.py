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
    
    if hsts:
        hsts_value = re.split('; |, ', hsts.lower())
        return { "enabled": True, "correct": True, "value": hsts_value }
    else:
        return { "enabled": False }
    
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
        xss_value = re.split('; |, ', xss.lower())
        
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
    
def check_refesh(headers: dict) -> dict:
    refresh = headers.get("refresh")
    
    if refresh:
        return {"enabled": True, "value": refresh}
    else:
        return {"enabled": False}   

def check_permissions(headers: dict) -> dict:
    permission = headers.get("permissions-policy")
    
    if permission:
        permission_value = re.split('; |, ', permission.lower())

        return {"enabled": True, "correct": True, "value": permission_value}
    else:
        return {"enabled": False, "correct": False}

def check_referrer(headers: dict) -> dict:
    referrer = headers.get("referrer-policy")
    
    if referrer:
        isCorrect = False
        referrer_value = re.split('; |, ', referrer.lower())
        
        if referrer_value not in ['no-referrer', 'strict-origin-when-cross-origin', 'no-referrer-when-downgrade', 'strict-origin']:
            isCorrect = True
            
        return {"enabled": True, "correct": isCorrect, "value": referrer_value}
    else:
        return {"enabled": False, "correct": False}

def check_cache(headers: dict) -> dict:
    cache = headers.get("cache-control")
    
    if cache:
        isCorrect = False
        cache_value = re.split('; |, ', cache.lower())
        
        if "no-store" in cache_value:
            isCorrect = True
            
        return {"enabled": True, "correct": isCorrect, "value": cache_value}
    else:
        return {"enabled": False, "correct": False}

def check_cookie(headers: dict) -> dict:
    cookie = headers.get("set-cookie")
    
    if cookie:
        cookie_value = re.split('; |, ', cookie.lower())
        isCorrect = False
        
        if "secure" in cookie_value and "httponly" in cookie_value:
            isCorrect = True
            
        return {"enabled": True, "correct": isCorrect, "value": cookie_value}
    else:
        return {"enabled": False}
    
def check_csp(headers: dict) -> dict:
    csp = headers.get("content-security-policy")
    
    if csp:
        csp_value = re.split('; |, ', csp.lower())
        return {"enabled": True, "correct": True, "value": csp_value}
    else:
        return {"enabled": False}
