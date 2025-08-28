from playwright.async_api import async_playwright

class WebPage:
    def __init__(self, url: str):
        self.domain = url.split('/')[0]
        self.url = url
        self.forms = []       
        self.links = []       
        self.meta_tags = []
        self.script_tags = []
        self.link_tags = []
        self.vulnerabilities = []
        self.content = None

    def add_form(self, form):
        self.forms.append(form)

    def add_link(self, link):
        self.links.append(link)

    def add_meta_tag(self, meta):
        self.meta_tags.append(meta)\

    def add_script_tag(self, script):
        self.script_tags.append(script)

    def add_link_tag(self, link):
        self.link_tags.append(link)

    def add_vulnerability(self, vulnerability):
        self.vulnerabilities.append(vulnerability)

    def get_meta_by_name(self, name: str):
        for meta in self.meta_tags:
            if meta.name and meta.name.lower() == name.lower():
                return meta
        return None

    def get_meta_by_http(self, http: str):
        for meta in self.meta_tags:
            if meta.http and meta.http.lower() == http.lower():
                return meta
        return None

    def get_meta_charset(self):
        for meta in self.meta_tags:
            if meta.charset:
                return meta
        return None

    async def load_webpage(self, url: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.wait_for_load_state("load")

            self.content = await page.content()

            await browser.close()

class MetaTag:
    def __init__(self, name: str, content: str, http: str, charset: str, code: str):
        self.name = name
        self.content = content
        self.http = http
        self.charset = charset
        self.code = code

class Form:
    def __init__(self, id: str, classname: list[str], action: str, method: str, code: str):
        self.id = id
        self.classname = classname
        self.action = action
        self.method = method
        self.fields = []
        self.form_type = None
        self.fields_count = {"total": 0}
        self.has_csrf = False
        self.has_captcha = False
        self.code = code

    def add_field(self, field):
        # Count fields types in a form
        if field.type != 'hidden':
            if field.type not in self.fields_count: self.fields_count[field.type] = 1
            else: self.fields_count[field.type] = self.fields_count[field.type] + 1
            self.fields_count["total"] = self.fields_count["total"] + 1
        # Check if input is related to captcha or csrf
        if field.id and 'csrf' in field.id or field.classname and 'csrf' in ''.join(field.classname).lower() or field.name and 'csrf' in field.name.lower():
            self.has_csrf = True
        if field.id and 'captcha' in field.id or field.classname and 'captcha' in ''.join(field.classname).lower() or field.name and 'captcha' in field.name.lower():
            self.has_captcha = True

        self.fields.append(field)

    def set_form_type(self, type: str):
        self.form_type = type
    
    def format_form_info(self) -> str:
        form_id = ""
        form_class = ""
        form_action = ""

        if self.id and self.id != "":
            form_id = f"{self.id.lower().replace('-', '').replace('_', '')} "
        if self.classname and len(self.classname) > 0:
            form_class = f"{" ".join(self.classname).lower().replace('-', '').replace('_', '')} "
        if self.action and self.action != "":
            form_action = self.action.lower().replace('-', '').replace('_', '')

        return f"{form_id}{form_class}{form_action}"

class Field:
    def __init__(self, id: str, classname: str, name: str, type: str, value: str, placeholder: str, code: str):
        self.id = id
        self.classname = classname
        self.name = name
        self.type = type
        self.value = value
        self.placeholder = placeholder
        self.code = code
    
    def format_field_info(self) -> str:
        field_id = ""
        field_class = ""
        field_name = ""

        if self.id and self.id != "":
            field_id = f"{self.id.lower().replace('-', '').replace('_', '')} "
        if self.classname and len(self.classname) > 0:
            field_class = f"{" ".join(self.classname).lower().replace('-', '').replace('_', '')} "
        if self.name and self.name != "":
            field_name = self.name.lower().replace('-', '').replace('_', '')

        return f"{field_id}{field_class}{field_name}"

class Link:
    def __init__(self, href: str, text: str, rel: str, target: str, code: str):
        self.href = href
        self.text = text
        self.rel = rel
        self.blank = self.is_blank(target)
        self.external = self.is_external(href)
        self.code = code

    def is_blank(self, target: str) -> bool:
        return target and target == "_blank"

    def is_external(self, href: str) -> bool:
        return href and href.startswith(("http://", "https://", "//"))
    
class ScriptTag:
    def __init__(self, src: str, type: str, external: bool, crossorigin: str, integrity: str, content: str, code: str):
        self.src = src
        self.inline = src is None or src == ""
        self.type = type
        self.external = external
        self.crossorigin = crossorigin
        self.integrity = integrity
        self.content = content
        self.code = code

class LinkTag:
    def __init__(self, href: str, rel: str, type: str, external: bool, integrity: str, crossorigin: str, code: str):
        self.href = href
        self.rel = rel
        self.type = type
        self.external = external
        self.integrity = integrity
        self.crossorigin = crossorigin
        self.code = code
    
class Vulnerability:
    def __init__(self, name: str, type: str, severity: str, details: str, location: str = "", code: str = ""):
        self.name = name
        self.type = type
        self.severity = severity
        self.location = location if location is not None else ""
        self.code = code if code is not None else ""
        self.details = details