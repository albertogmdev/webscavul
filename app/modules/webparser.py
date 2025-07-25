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
        meta_name = meta.get('name', '').lower()
        meta_content = meta.get('content', '')
        if meta_name and meta_content:
            print('META: ', meta_name, meta_content)
            webpage.add_meta_tag(MetaTag(meta_name, meta_content))

def parse_forms(soup: BeautifulSoup, webpage: WebPage):
    print("INFO: Parsing forms in the webpage")
    form_index = 1
    for form in soup.find_all('form'):
        form_id = form.get('id')
        if not form_id:
            form_id = f'form:nth-child({form_index})'
        form_method = form.get('method')
        if form_method:
            form_method = form_method.upper()
        form_action = form.get('action')
        form_fields = parse_fields(form)
        
        print('FORM: ', form_id, form_action, form_method)
        webpage.add_form(Form(form_id, form_action, form_method, form_fields))
        form_index += 1

def parse_fields(form: BeautifulSoup):
    fields = []
    for field in form.find_all(['input', 'select', 'textarea']):
        field_name = field.get('name')
        field_type = field.get('type', 'text')
        field_value = field.get('value', '')
        field_placeholder = field.get('placeholder', '')

        print('FIELD: ', field_name, field_type, field_value, field_placeholder)
        fields.append(Field(field_name, field_type, field_value, field_placeholder, field))
    
    return fields

def parse_links(soup: BeautifulSoup, webpage: WebPage):
    print("INFO: Parsing links in the webpage")
    for link in soup.find_all('a'):
        link_href = link.get('href')
        link_text = link.get_text().strip()
        link_target = link.get('target')
        link_rel = link.get('rel')

        print('LINK: ', link_href, link_text, link_rel, link_target)
        webpage.add_link(Link(link_href, link_text, link_rel, link_target, link))

def parse_linktags(soup: BeautifulSoup, webpage: WebPage):
    print("INFO: Parsing link tags in the webpage")
    for link in soup.find_all('link'):
        link_href = link.get('href')
        link_rel = link.get('rel')
        link_type = link.get('type')
        link_integrity = link.get('integrity')
        link_crossorigin = link.get('crossorigin')
        link_referrer
        link_external = link_href and webpage.domain not in link_href and not link_href.startswith('/')

        print('LINKTAG: ', link_href, link_rel, link_type, link_integrity, link_crossorigin, link_external)
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

        print('SCRIPT: ', script_src, script_type, script_crossorigin, script_integrity, script_external)
        webpage.add_script_tag(ScriptTag(script_src, script_type, script_external, script_crossorigin, script_integrity, script_content, script))
        