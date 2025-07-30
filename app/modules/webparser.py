import app.utils.utils as utils

from app.core.webpage import WebPage, MetaTag, Form, Field, Link, ScriptTag, LinkTag
from bs4 import BeautifulSoup

def parse_webpage(webpage: WebPage):
    if not webpage.content:
        return {}
    
    soup = BeautifulSoup(webpage.content, 'html.parser')

    parse_forms(soup, webpage)
    parse_links(soup, webpage) 
    parse_metatags(soup, webpage)
    parse_scripttags(soup, webpage)
    parse_linktags(soup, webpage)

def parse_metatags(soup: BeautifulSoup, webpage: WebPage):
    print("INFO: Parsing metas in the webpage")
    for meta in soup.find_all('meta'):
        meta_name = meta.get('name')
        meta_content = meta.get('content')
        meta_http = meta.get('http-equiv')
        meta_charset = meta.get('charset')
        if meta_name and meta_content or meta_http or meta_charset:
            print('[META]', meta_name, meta_content, meta_http, meta_charset)
            webpage.add_meta_tag(MetaTag(meta_name, meta_content, meta_http, meta_charset, meta))

def parse_forms(soup: BeautifulSoup, webpage: WebPage):
    print("INFO: Parsing forms in the webpage")
    form_index = 1
    for form in soup.find_all('form'):
        form_id = form.get('id')
        form_class = form.get('class')
        if not form_id:
            form_id = f'form:nth-child({form_index})'
        form_method = form.get('method')
        if form_method:
            form_method = form_method.upper()
        form_action = form.get('action')

        formObject = Form(form_id, form_class, form_action, form_method)

        parse_fields(form, formObject)
        form_type = determine_formtype(formObject)

        if form_type: 
            formObject.set_form_type(form_type)

        print('[FORM]', form_id, form_action, form_method)
        webpage.add_form(formObject)

        form_index += 1

def parse_fields(form: BeautifulSoup, formObject: Form):
    for field in form.find_all(['input', 'select', 'textarea']):
        field_id = field.get('id')
        field_class = field.get('class')
        field_name = field.get('name')
        field_type = field.get('type', 'text')
        if field.name == 'select' or field.name == 'textarea': field_type = field.name
        field_value = field.get('value', '')
        field_placeholder = field.get('placeholder', '')

        print('[FIELD]', field_id, field_class, field_name, field_type, field_value, field_placeholder)
        formObject.add_field(Field(field_id, field_class, field_name, field_type, field_value, field_placeholder, field))

def parse_links(soup: BeautifulSoup, webpage: WebPage):
    print("INFO: Parsing links in the webpage")
    for link in soup.find_all('a'):
        link_href = link.get('href')
        link_text = link.get_text().strip()
        link_target = link.get('target')
        link_rel = link.get('rel')

        print('[LINK]', link_href, link_text, link_rel, link_target)
        webpage.add_link(Link(link_href, link_text, link_rel, link_target, link))

def parse_linktags(soup: BeautifulSoup, webpage: WebPage):
    print("INFO: Parsing link tags in the webpage")
    for link in soup.find_all('link'):
        link_href = link.get('href')
        link_rel = link.get('rel')
        link_type = link.get('type')
        link_integrity = link.get('integrity')
        link_crossorigin = link.get('crossorigin')
        link_external = link_href and webpage.domain not in link_href and not link_href.startswith('/')

        print('[LINKTAG]', link_href, link_rel, link_type, link_integrity, link_crossorigin, link_external)
        webpage.add_link_tag(LinkTag(link_href, link_rel, link_type, link_external, link_integrity, link_crossorigin, link))

def parse_scripttags(soup: BeautifulSoup, webpage: WebPage):
    print("INFO: Parsing scripts in the webpage")
    for script in soup.find_all('script'):
        script_src = script.get('src')
        script_type = script.get('type')
        script_crossorigin = script.get('crossorigin')
        script_integrity = script.get('integrity')
        script_content = script.string
        script_external = script_src and webpage.domain not in script_src and not script_src.startswith('/')

        print('[SCRIPT]', script_src, script_type, script_crossorigin, script_integrity, script_external)
        webpage.add_script_tag(ScriptTag(script_src, script_type, script_external, script_crossorigin, script_integrity, script_content, script))
        
def determine_formtype(form: Form):
    form_type = None
    keywords = {
        "login": ["login", "signin", "auth", "access", "identify", "acceso", "acceder", "entrar", "identificacion", "identificar", "autenticar", "autenticacion", "iniciosesion", "iniciarsesion"],
        "signup": ["register", "signup", "createaccount", "newaccount", "accountnew", "join", "registro", "registrar", "crearcuenta", "nuevacuenta", "cuentanueva", "registrarme", "alta", "unirse", "unirme"],
        "search": ["search", "query", "find", "busqueda", "buscar", "buscador"],
        "contact": ["contact", "message", "inquiry", "feedback",  "support", "help", "contacto", "ayuda", "soporte", "consulta"],

    }
    types = {
        "login": 0,
        "signup": 0,
        "search": 0,
        "contact": 0
    }

    print(form.fields_count)
    total_count = form.fields_count["total"]
    # Checkt form id, action and classes
    formated_info = form.format_form_info()
    if formated_info and formated_info != "":   
        for type, values in keywords.items():
            for keyword in values:
                if keyword in formated_info: 
                    types[type] += 10
                    break

    # Heuristic for login form
    if total_count <= 5 and total_count >= 2: types["login"] += 2
    else: types["login"] -= 3
    # Heuristic for signup form
    if total_count <= 5 and total_count >= 2: types["signup"] += 2
    # Heuristic for search form, usually a 2 or 3 inputs, with a text/search input and maybe a submit
    allowed_search_inputs = ["search", "text", "submit"]
    if total_count <= 3: types["search"] += 2
    else: types["search"] -= 3
    for input in form.fields_count: 
        if input == "search": types["search"] += 5
        elif input not in allowed_search_inputs: types["search"] -= 1
    # Heuristic for contact form


    max_value = -100
    selected_type = None
    multiple_types = False
    for type, value in types.items():
        if value > max_value:
            max_value = value
            selected_type = type
            multiple_types = False
        if value == max_value and value > 0:
            multiple_types = True
    
    print(types)
    print(formated_info)
    print(selected_type)

    return form_type