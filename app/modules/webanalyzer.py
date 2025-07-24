from app.core.webpage import WebPage, MetaTag, Form, Field, Link, Vulnerability

from bs4 import BeautifulSoup

def analyze_webpage(webpage: WebPage):
    print("INFO: Analyzing webpage content")

    analyze_forms(webpage)
    analyze_scripts(webpage)
    analyze_metatags(webpage)
    analyze_links(webpage)

    result = {}
    for vulnerability in webpage.vulnerabilities:
        result[vulnerability.type] = vulnerability.location
    return result

def analyze_forms(webpage: WebPage):
    print("INFO: Analyzing forms in the webpage")

def analyze_scripts(webpage: WebPage):
    print("INFO: Analyzing scripts in the webpage")

def analyze_metatags(webpage: WebPage):
    print("INFO: Analyzing metatags in the webpage")

def analyze_links(webpage: WebPage):
    print("INFO: Analyzing links in the webpage")

    for link in webpage.links:
        # Link externo inseguro
        if link.href and link.href != '' and link.href.startswith('http://'):
            print('hola')
            webpage.add_vulnerability(
                Vulnerability(
                    name="Link externo inseguro (HTTP)",
                    type="Link",
                    severity="Low",
                    location=link.href,
                    details="El enlace apunta a un recurso externo utilizando HTTP en lugar de HTTPS.",
                )
            )
        # Link con target _blank sin rel="noopener noreferrer"
        if link.blank and (link.rel is None or (link.rel is not None and "noopener" not in link.rel or "noreferrer" not in link.rel)):
            webpage.add_vulnerability(
                Vulnerability(
                    name="Link con target _blank sin rel='noopener'",
                    type="Link",
                    severity="Medium",
                    location="",
                    details="El enlace tiene un target '_blank' sin el atributo 'rel' adecuado, lo que puede permitir ataques de phishing.",
                )
            )