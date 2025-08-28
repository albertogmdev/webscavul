from core.webpage import WebPage, Vulnerability
import re

def analyze_webpage(webpage: WebPage, headers: dict) -> dict:
    print("INFO: Analyzing webpage content")

    analyze_metatags(webpage, headers)
    analyze_forms(webpage)
    analyze_script_tags(webpage)
    analyze_link_tags(webpage)
    analyze_links(webpage)

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
                code=form.code,
                details="El formulario no tiene implementado el token CSRF, esto puede ocasionar o facilitar los ataques de secuestro de sesión. Se recomienda la implementación de este token en formularios críticos (inicio de sesión, creación de cuentas...)",
            ))
        
        # Action with HTTP url
        if form.action and form.action.startswith('http://'):
            webpage.add_vulnerability(Vulnerability(
                name="Form con atributo 'action' externo inseguro (HTTP)",
                type="Form",
                severity="High",
                location=f"{form.id} action: [${form.action}]",
                code=form.code,
                details="El formulario tiene implementado el atributo 'action' con una URL que referencia a un posible sitio externo malicioso o inseguro, debido a que este implementa HTTPS. ",
            ))

        # Form with sensitive data without proper method 
        if (not form.method or form.method.lower() == 'get' or form.method == '') and 'password' in form.fields_count:
            webpage.add_vulnerability(Vulnerability(
                name="Formulario con datos confidenciales expuestos (GET)",
                type="Form",
                severity="High",
                location=f"{form.id} method: [${form.method}]",
                code=form.code,
                details="El formulario procesa datos confidenciales, como contraseñas, implementando un método que no guarda la confidencialidad de los datos (GET). El método GET expone de texto claro los datos del formulario, quedando estos expuestos a terceros.",
            ))
        
        # Form without action atribute
        if not form.action or form.action == '':
            webpage.add_vulnerability(Vulnerability(
                name="Formulario con atributo 'action' vacío",
                type="Form",
                severity="Information",
                location=form.id,
                code=form.code,
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
                        code=form.code,
                        details="El formulario contiene un campo de contraseña que no utiliza el tipo de input adecuado (password). Esto puede exponer la contraseña en texto plano al escribirla, facilitando que sea visible para terceros. Se recomienda establecer el tipo password para proteger la confidencialidad del dato."
                    ))
                    if not form.method or form.method.lower() == 'get' or form.method == '':
                        webpage.add_vulnerability(Vulnerability(
                            name="Form con datos confidenciales expuestos (GET)",
                            type="Form",
                            severity="High",
                            location=form.id,
                            code=form.code,
                            details="El formulario procesa datos confidenciales, como contraseñas, implementando un método que no guarda la confidencialidad de los datos (GET). El método GET expone de texto claro los datos del formulario, quedando estos expuestos a terceros.",
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
                details="El script apunta a un recurso externo utilizando HTTP en lugar de HTTPS, lo que puede indicar que el recurso pertenece a un sitio inseguro o malicioso. Esto puede permitir ataques de phishing o inyección de código malicioso. Si este sitio no es conocido, se recomienda utilizar HTTPS para todos los recursos externos de la página web.",
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
                    details="El script externo no cuenta con los atributos integrity y/o crossorigin configurados correctamente. Esto impide verificar que el archivo no ha sido alterado, lo que puede facilitar la inyección de código malicioso. Se recomienda habilitarlos para garantizar la integridad y seguridad del recurso.",
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
                    location=link.href,
                    code=link.code,
                    details="La etiqueta <link> apunta a un recurso externo utilizando HTTP en lugar de HTTPS.",
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
                        severity="Low",
                        location=link.href,
                        code=link.code,
                        details="La etiqueta <link> no cuenta con los atributos integrity y/o crossorigin configurados correctamente. Esto impide verificar que el archivo no ha sido alterado, lo que puede facilitar la inyección de código malicioso. Se recomienda habilitarlos para garantizar la integridad y seguridad del recurso.",
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
                        location={separator.join(attributes)},
                        code=link.code,
                        details=f"La etiqueta <link> usa los atributos {separator.join(attributes)} que ya no son recomendados por los estándares web. Aunque no representan un riesgo directo de seguridad, pueden afectar la compatibilidad y funcionamiento de la página en el futuro. Se recomienda actualizarlos siguiendo las especificaciones actuales de HTML.",
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
                details="La página no cuenta con una política de seguridad de contenidos (CSP). Este mecanismo ayuda a prevenir ataques como la inyección de scripts maliciosos (XSS) controlando qué recursos se pueden cargar. Se recomienda definir una CSP adecuada para reforzar la seguridad del sitio.",
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
                        code=meta_refresh,
                        details="La cabecera 'Refresh' redirige a un recurso o sitio externo inseguro o malicioso utilizando HTTP en lugar de HTTPS. Esto puede permitir ataques de phishing a dominios inseguros. Si el recurso no es conocido, se recomienda utilizar HTTPS para todos los recursos externos de la página web.",
                    ))
                elif url:
                    webpage.add_vulnerability(Vulnerability(
                        name=f"{'Meta tag' if is_header else 'Header'} tag Refresh activada",
                        type=f"{'Meta' if is_header else 'Header'}",
                        severity="Information",
                        location=url,
                        code=meta_refresh,
                        details="La cabecera o meta tag Refresh está activa. Aunque no siempre es peligrosa, puede ser usada para redirigir de forma automática a páginas maliciosas. Se recomienda evitar su uso y, en su lugar, gestionar las redirecciones desde el servidor de manera controlada.",
                    ))
    
    # Charset meta tag
    meta_charset = webpage.get_meta_charset()
    if not meta_charset:
        webpage.add_vulnerability(
            Vulnerability(
                name="Meta tag charset no configurada",
                type="Meta",
                severity="Medium",
                location="charset",
                details="La página no tiene configurada la meta tag 'charset'. Esto puede causar problemas de codificación y vulnerabilidades de seguridad. Se recomienda establecerla explícitamente en utf-8 para garantizar una correcta interpretación de los caracteres.",
            )
        )
    elif meta_charset.charset.lower() != "utf-8":
        webpage.add_vulnerability(
            Vulnerability(
                name="Meta tag charset con valor no recomendado",
                type="Meta",
                severity="Information",
                location=meta_charset.charset,
                code=meta_charset.code,
                details="La meta tag 'charset' está configurada con un valor diferente a 'utf-8'. Este formato es recomendado y ampliamente utilizado para evitar problemas de codificación.",
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
            details="La página no tiene configurada la meta tag 'robots'. Este atributo permite controlar como los motores de búsqueda indexan las rutas de la página web. Se recomienda establecerla para evitar que se indexen rutas sensibles o privadas.",
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
            location="referrer",
            details="La cabecera o meta tag referrer no está configurada. Esto puede provocar que el navegador envíe información sensible de la URL al sitio de destino, exponiendo datos a terceros. Se recomienda definir un valor seguro para limitar la información compartida.",
        ))
    elif meta_referrer and meta_referrer.lower() not in ['no-referrer', 'strict-origin-when-cross-origin', 'no-referrer-when-downgrade', 'strict-origin']:
        webpage.add_vulnerability(Vulnerability(
            name=f"{'Meta tag' if is_header else 'Header'} referrer con valor no recomendado",
            type=f"{'Meta' if is_header else 'Header'}",
            severity="Medium",
            details="La cabecera o meta tag referrer utiliza un valor no recomendado. Esto puede permitir la filtración innecesaria de datos a otros sitios. Se recomienda utilizar valores seguros como 'no-referrer', 'strict-origin-when-cross-origin', 'no-referrer-when-downgrade' o 'strict-origin'.",
        ))

    # generator meta tag
    meta_generator = webpage.get_meta_by_name("generator")
    if meta_generator and meta_generator.content and meta_generator.content != "":
        webpage.add_vulnerability(Vulnerability(
            name="Meta tag generator encontrada",
            type="Meta",
            severity="Information",
            location=meta_generator.content,
            code=meta_generator.code,
            details="La meta tag 'generator' puede revelar información sobre el CMS o framework utilizado, lo que podría ser útil y dar información relevante al atacante para un atacante.",
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
                code=link.code,
                details="El enlace apunta a un recurso externo utilizando HTTP en lugar de HTTPS, lo que puede indicar que el recurso pertenece a un sitio inseguro o malicioso. Esto puede permitir que los usuarios accedan a páginas con ataques de phishing o inyección de código malicioso. Si este sitio no es conocido, se recomienda utilizar HTTPS para todos los recursos externos de la página web.",
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
                    code=link.code,
                    details="El enlace tiene un target '_blank' sin el atributo 'rel' recomendado, Esto puede permitir que la página abierta manipule la original, facilitando ataques de phishing o robo de información. Se aconseja añadir rel="'oopener noreferrer'" para mitigar este riesgo.",
                ))