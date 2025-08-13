from core.webpage import WebPage, Vulnerability
import re

def analyze_webpage(webpage: WebPage, headers: dict) -> dict:
    print("INFO: Analyzing webpage content")

    analyze_metatags(webpage, headers)
    analyze_forms(webpage)
    analyze_script_tags(webpage)
    analyze_link_tags(webpage)
    analyze_links(webpage)

    result = {}
    for index, vulnerability in enumerate(webpage.vulnerabilities):
        result[f"{vulnerability.type}-{index}"] = {
            "nombre": vulnerability.name,
            "text": vulnerability.location
        }
    return result

def analyze_forms(webpage: WebPage):
    print("INFO: Analyzing forms in the webpage")
    
    for form in webpage.forms:
        # CSRF Token not present
        if not form.has_csrf and not form.has_captcha:
            form_type = form.form_type
            severity = 'High' if form_type not in ["login", "signup"] else 'Information'
            webpage.add_vulnerability(Vulnerability(
                name=f"Formulario sin token CSRF implementado",
                type="Form",
                severity=severity,
                location=form.id,
                details="",
            ))
        
        # Action with HTTP url
        if form.action and form.action.startswith('http://'):
            webpage.add_vulnerability(Vulnerability(
                name="Form con atributo 'action' externo inseguro (HTTP)",
                type="Form",
                severity="High",
                location=form.action,
                details="",
            ))

        # Form with sensitive data without proper method 
        if (not form.method or form.method.lower() == 'get' or form.method == '') and 'password' in form.fields_count:
            webpage.add_vulnerability(Vulnerability(
                name="Formulario con datos confidenciales expuestos (GET)",
                type="Form",
                severity="High",
                location=form.method,
                details="",
            ))
        
        # Form without action atribute
        if not form.action or form.action == '':
            webpage.add_vulnerability(Vulnerability(
                name="Formulario con atributo 'action' vacío",
                type="Form",
                severity="Information",
                location=form.id,
                details="Se recomienda especificar explícitamente el valor del atributo 'action' para mejorar la claridad del código, la mantenibilidad y evitar posibles confusiones. El formulario enviará los datos a la misma URL de la página."
            ))

        # Input with keyword password but not type password, also check form action
        password_keyword = ["password", "pwd", "passwd", "contrasena", "contrasenna", "contraseña"]
        for field in form.fields:
            if field.type in ["text", "textarea"]:
                formated_info = field.format_field_info() 
                if any(keyword in formated_info for keyword in password_keyword):
                    webpage.add_vulnerability(Vulnerability(
                        name="Formulario con campo de contraseña sin usar tipo de input correcto (password)",
                        type="Form",
                        severity="Medium",
                        location=form.id,
                        details=""
                    ))
                    if not form.method or form.method.lower() == 'get' or form.method == '':
                        webpage.add_vulnerability(Vulnerability(
                            name="Form con datos confidenciales expuestos (GET)",
                            type="Form",
                            severity="High",
                            location=form.id,
                            details="",
                        ))


def analyze_script_tags(webpage: WebPage):
    print("INFO: Analyzing script tags in the webpage")

    for script in webpage.script_tags:
        # Script externo inseguro
        if script.src and script.external and script.src.startswith('http://'):
            webpage.add_vulnerability(Vulnerability(
                name="Script externo inseguro (HTTP)",
                type="Script",
                severity="Low",
                location=script.src,
                code=script.code,
                details="El script apunta a un recurso externo utilizando HTTP en lugar de HTTPS.",
            ))
        # Script con SRI configurado de forma incorrecta
        sri_value = ""
        if script.src is not None and script.src != "" and script.external:
            if not script.crossorigin and not script.integrity: sri_value = "sin crossorigin ni integrity"
            elif script.crossorigin and not script.integrity: sri_value = "con crossorigin sin integrity"
            elif script.integrity and not script.crossorigin: sri_value = "con integrity sin crossorigin"
            if sri_value != "":
                webpage.add_vulnerability(Vulnerability(
                    name=f"Script {sri_value}",
                    type="Script",
                    severity="Medium",
                    location=script.src,
                    code=script.code,
                    details="El script no tiene los atributos 'crossorigin' e 'integrity', lo que puede permitir ataques de inyección.",
                ))

def analyze_link_tags(webpage: WebPage):
    print("INFO: Analyzing link tags in the webpage")

    deprecated_attributes = ['charset', 'rev']
    for link in webpage.link_tags:
        # Link externo inseguro
        if link.href and link.href != '' and link.href.startswith('http://'):
            webpage.add_vulnerability(
                Vulnerability(
                    name="Link externo inseguro (HTTP)",
                    type="Link",
                    severity="Low",
                    location=f"{link.code}",
                    details="Link tag apunta a un recurso externo utilizando HTTP en lugar de HTTPS.",
                )
            )
        # Link con SRI configurado de forma incorrecta
        sri_value = ""
        if link.href is not None and link.href != "" and link.external:
            if not link.crossorigin and not link.integrity: sri_value = "sin crossorigin ni integrity"
            elif link.crossorigin and not link.integrity: sri_value = "con crossorigin sin integrity"
            elif link.integrity and not link.crossorigin: sri_value = "con integrity sin crossorigin"
            if sri_value != "":
                webpage.add_vulnerability(
                    Vulnerability(
                        name=f"Link {sri_value}",
                        type="Link",
                        severity="Medium",
                        location=f"{link.code}",
                        details="Link tag no tiene los atributos 'crossorigin' e 'integrity', lo que puede permitir ataques de inyección.",
                    )
                )
        # Link con atributes deprecated
        attributes = []
        for attribute in deprecated_attributes:
            if f"{attribute}=" in link.code: attributes.append(attribute)
        if len(attributes) > 0: 
            separator = ','
            webpage.add_vulnerability(
                    Vulnerability(
                        name=f"Link con atributos {separator.join(attributes)} deprecados",
                        type="Link",
                        severity="Medium",
                        location=f"{link.code}",
                        details=f"Link tag contiene los atributos deprecated {separator.join(attributes)}.",
                    )
                )

def analyze_metatags(webpage: WebPage, headers: dict):
    print("INFO: Analyzing metatags in the webpage")
    
    # CSP meta tag
    meta_csp = webpage.get_meta_by_http("Content-Security-Policy")
    if not headers['csp']['enabled']:
        if not meta_csp:
            webpage.add_vulnerability(Vulnerability(
                name="Meta tag CSP no configurada",
                type="Meta",
                severity="High",
                location="Content-Security-Policy",
                details="La página no tiene configurada la meta tag 'Content-Security-Policy'.",
            ))
    
    # Refresh meta tag / header
    meta_refresh = None
    is_header = False
    if not headers['refresh']['enabled']: 
        meta_refresh = webpage.get_meta_by_http("Refresh")
        if meta_refresh: meta_refresh = meta_refresh.content
    else: 
        is_header = True
        meta_refresh = headers['refresh']['value']
    if meta_refresh:
        values = re.split('; |, ', meta_refresh.lower())
        for value in values:
            if value.startswith('url='):
                split_value = value.split('=')
                url = None
                if len(split_value) > 1:
                    url = split_value[1]
                if url and url.startswith(('http://')):
                    webpage.add_vulnerability(Vulnerability(
                        name=f"{'Meta tag' if is_header else 'Header'} refresh con valor de redirección inseguro (HTTP)",
                        type=f"{'Meta' if is_header else 'Header'}",
                        severity="High",
                        location=url,
                        details="La cabecera 'Refresh' redirige a un recurso externo utilizando HTTP en lugar de HTTPS. Esto puede permitir ataques de phishing a dominios inseguros.",
                    ))
                elif url:
                    webpage.add_vulnerability(Vulnerability(
                        name=f"{'Meta tag' if is_header else 'Header'} tag Refresh activada",
                        type=f"{'Meta' if is_header else 'Header'}",
                        severity="Information",
                        location=url,
                        details="El uso de la cabecera 'Refresh' puede ser problemático, ya que puede permitir ataques de phishing.",
                    ))
    
    # Charset meta tag
    meta_charset = webpage.get_meta_charset()
    if not meta_charset:
        webpage.add_vulnerability(
            Vulnerability(
                name="Meta tag charset no configurada",
                type="Meta",
                severity="Medium",
                location="",
                details="La página no tiene configurada la meta tag 'charset'. Esto puede causar problemas de codificación y vulnerabilidades de seguridad.",
            )
        )
    elif meta_charset.charset.lower() != "utf-8":
        webpage.add_vulnerability(
            Vulnerability(
                name="Meta tag charset con valor no recomendado",
                type="Meta",
                severity="Information",
                location=meta_charset.charset,
                details="La meta tag 'charset' no está configurada como 'utf-8'. Este formato es recomendado y ampliamente utilizado para evitar problemas de codificación.",
            )
        )
    
    # robots meta tag
    meta_robots = webpage.get_meta_by_name("robots")
    if not meta_robots:
        webpage.add_vulnerability(Vulnerability(
            name="Meta tag robots no configurada",
            type="Meta",
            severity="Information",
            location="robots",
            details="La página no tiene configurada la meta tag 'robots'. Especificarlo otorga un mayor control sobre la indexación de las páginas.",
        ))
   
    meta_referrer = None
    is_header = False
    if not headers['referrer']['enabled'] or headers['referrer']['enabled'] and not headers['referrer']['correct']: 
        meta_referrer = webpage.get_meta_by_name("referrer")
        if meta_referrer: meta_referrer = meta_referrer.content
    else:
        meta_referrer = headers['referrer']['value']
        is_header = True
    
    if not meta_referrer:
        webpage.add_vulnerability(Vulnerability(
            name="Meta tag / Header referrer no configurado",
            type="Meta",
            severity="Medium",
            location="",
            details="Referrer no está configurado, lo que puede provocar que el navegador establezca un valor de referrer inseguro.",
        ))
    elif meta_referrer and meta_referrer.lower() not in ['no-referrer', 'strict-origin-when-cross-origin', 'no-referrer-when-downgrade', 'strict-origin']:
        webpage.add_vulnerability(Vulnerability(
            name=f"{'Meta tag' if is_header else 'Header'} referrer con valor no recomendado",
            type=f"{'Meta' if is_header else 'Header'}",
            severity="Medium",
            location=meta_referrer,
            details="El valor de 'referrer' no es recomendado. Se recomienda utilizar valores como 'no-referrer', 'strict-origin-when-cross-origin', 'no-referrer-when-downgrade' o 'strict-origin'.",
        ))

    # generator meta tag
    meta_generator = webpage.get_meta_by_name("generator")
    if meta_generator and meta_generator.content and meta_generator.content != "":
        webpage.add_vulnerability(Vulnerability(
            name="Meta tag generator encontrada",
            type="Meta",
            severity="Information",
            location=meta_generator.content,
            details="La meta tag 'generator' puede revelar información sobre el CMS o framework utilizado, lo que podría ser útil para un atacante.",
        ))

def analyze_links(webpage: WebPage):
    print("INFO: Analyzing links in the webpage")

    for link in webpage.links:
        # Enlace externo inseguro
        if link.href and link.href != '' and link.href.startswith('http://'):
            webpage.add_vulnerability(Vulnerability(
                name="Enlace externo inseguro (HTTP)",
                type="Enlace",
                severity="Low",
                location=link.href,
                details="El enlace apunta a un recurso externo utilizando HTTP en lugar de HTTPS.",
            ))
        # Link con target _blank sin rel="noopener noreferrer"
        rel_value = ""
        if link.blank and link.href is not None and link.href != "" and link.external:
            if link.rel is None or link.rel is not None and "noopener" not in link.rel and "noreferrer" not in link.rel: rel_value = "rel=noopener noreferrer"
            elif "noopener" not in link.rel: rel_value = "rel=noopener"
            elif "noreferrer" not in link.rel: rel_value = "rel=noreferrer"

            if rel_value != "":
                webpage.add_vulnerability(Vulnerability(
                    name=f"Enlace con target _blank sin {rel_value}",
                    type="Enlace",
                    severity="Medium",
                    location=link.href,
                    details="El enlace tiene un target '_blank' sin el atributo 'rel' adecuado, lo que puede permitir ataques de phishing.",
                ))