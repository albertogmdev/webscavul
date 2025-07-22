from app.core.webpage import WebPage, MetaTag, Form, Field, Link, Vulnerability

from bs4 import BeautifulSoup

def parse_webpage(webpage: WebPage):
    if not webpage.content:
        return {}
    
    soup = BeautifulSoup(webpage.content, 'html.parser')

    parse_forms(soup, webpage)
    parse_links(soup, webpage) 
    parse_metatags(soup, webpage)

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
        
        print('FORM: ', form_id, form_action, form_method)
        print(form)
        webpage.add_form(Form(form_id, form_action, form_method, form))
        form_index += 1

def parse_links(soup: BeautifulSoup, webpage: WebPage):
    print("INFO: Parsing links in the webpage")
    for link in soup.find_all('a'):
        link_href = link.get('href')
        link_text = link.get_text().strip()
        link_target = link.get('target')
        link_rel = link.get('rel')

        print('LINK: ', link_href, link_text, link_rel, link_target)
        webpage.add_link(Link(link_href, link_text, link_rel, link_target, link))
        