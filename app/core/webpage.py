from playwright.async_api import async_playwright

class WebPage:
    def __init__(self, domain: str):
        self.domain = domain
        self.forms = []       
        self.links = []       
        self.meta_tags = []
        self.scripts = []
        self.vulnerabilities = []
        self.content = None

    def add_form(self, form):
        self.forms.append(form)

    def add_link(self, link):
        self.links.append(link)

    def add_meta_tag(self, meta):
        self.meta_tags = meta

    def add_script(self, script):
        self.scripts.append(script)

    def add_vulnerability(self, vulnerability):
        self.vulnerabilities.append(vulnerability)

    async def load_webpage(self, url: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.wait_for_load_state("load")

            try:
                #TODO : Manejar el popup de las cookies
                await page.wait_for_selector('text=Deny', state='visible', timeout=1000)
                await page.click('text=Deny')
                print("Botón 'Deny' clickeado exitosamente.")
                #await page.screenshot(path="clicked_screenshot.png")
            except Exception as e:
                print(f"No se pudo clickear el botón 'Deny': {e}")
                #await page.screenshot(path="error_click_screenshot.png")

            self.content = await page.content()

            await browser.close()

class MetaTag:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

class Form:
    def __init__(self, id: str, action: str, method: str, fields: str):
        self.id = id
        self.action = action
        self.method = method
        self.fields = fields

    def add_field(self, field):
        self.fields.append(field)

class Field:
    def __init__(self, name: str, type: str, value: str, placeholder: str, code: str):
        self.name = name
        self.type = type
        self.value = value
        self.placeholder = placeholder
        self.code = code

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
        return href and not href.startswith(self.href.split('/')[0])
    
class Script:
    def __init__(self, src: str, type: str, external: bool, crossorigin: str, integrity: str, content: str, code: str):
        self.src = src
        self.inline = src is None or src == ""
        self.type = type
        self.external = external
        self.crossorigin = crossorigin
        self.integrity = integrity
        self.content = content
        self.code = code
    
    
class Vulnerability:
    def __init__(self, name: str, type: str, severity: str, location: str, details: str, payload: str = ""):
        self.name = name
        self.type = type
        self.severity = severity
        self.location = location
        self.details = details
        self.payload = payload