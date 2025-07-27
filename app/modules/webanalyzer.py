from app.core.webpage import WebPage, MetaTag, Form, Field, Link, Vulnerability

from bs4 import BeautifulSoup

def analyze_webpage(webpage: WebPage):
    print("INFO: Analyzing webpage content")

    analyze_forms(webpage)
    analyze_script_tags(webpage)
    analyze_link_tags(webpage)
    analyze_metatags(webpage)
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

def analyze_script_tags(webpage: WebPage):
    print("INFO: Analyzing script tags in the webpage")

    for script in webpage.script_tags:
        # Script externo inseguro
        if script.src and script.external and script.src.startswith('http://'):
            webpage.add_vulnerability(
                Vulnerability(
                    name="Script externo inseguro (HTTP)",
                    type="Script",
                    severity="Low",
                    location=script.src,
                    details="El script apunta a un recurso externo utilizando HTTP en lugar de HTTPS.",
                )
            )
        # Script con SRI configurado de forma incorrecta
        sri_value = ""
        if script.src is not None and script.src != "" and script.external:
            if not script.crossorigin and not script.integrity: sri_value = "sin crossorigin ni integrity"
            elif script.crossorigin and not script.integrity: sri_value = "con crossorigin sin integrity"
            elif script.integrity and not script.crossorigin: sri_value = "con integrity sin crossorigin"
            if sri_value != "":
                webpage.add_vulnerability(
                    Vulnerability(
                        name=f"Script {sri_value}",
                        type="Script",
                        severity="Medium",
                        location=script.src,
                        details="El script no tiene los atributos 'crossorigin' e 'integrity', lo que puede permitir ataques de inyección.",
                    )
                )

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

def analyze_metatags(webpage: WebPage):
    print("INFO: Analyzing metatags in the webpage")

    for meta in webpage.meta_tags:
        print(meta.name, meta.content, meta.http)

def analyze_links(webpage: WebPage):
    print("INFO: Analyzing links in the webpage")

    for link in webpage.links:
        # Enlace externo inseguro
        if link.href and link.href != '' and link.href.startswith('http://'):
            webpage.add_vulnerability(
                Vulnerability(
                    name="Enlace externo inseguro (HTTP)",
                    type="Enlace",
                    severity="Low",
                    location=link.href,
                    details="El enlace apunta a un recurso externo utilizando HTTP en lugar de HTTPS.",
                )
            )
        # Link con target _blank sin rel="noopener noreferrer"
        rel_value = ""
        if link.blank and link.href is not None and link.href != "" and link.external:
            if link.rel is None or link.rel is not None and "noopener" not in link.rel and "noreferrer" not in link.rel: rel_value = "rel=noopener noreferrer"
            elif "noopener" not in link.rel: rel_value = "rel=noopener"
            elif "noreferrer" not in link.rel: rel_value = "rel=noreferrer"

            if rel_value != "":
                webpage.add_vulnerability(
                    Vulnerability(
                        name=f"Enlace con target _blank sin {rel_value}",
                        type="Enlace",
                        severity="Medium",
                        location=link.href,
                        details="El enlace tiene un target '_blank' sin el atributo 'rel' adecuado, lo que puede permitir ataques de phishing.",
                    )
                )