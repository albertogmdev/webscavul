from playwright.async_api import async_playwright

class WebPage:
    def __init__(self):
        self.content = None
        self.forms = []       
        self.links = []       
        self.meta_tags = []
        self.vulnerabilities = []

    def add_form(self, form):
        self.forms.append(form)

    def add_link(self, link):
        self.links.append(link)

    def add_meta_tag(self, meta):
        self.meta_tags = meta

    def add_vulnerability(self, vulnerability):
        self.vulnerabilities.append(vulnerability)

    async def load_webpage(self, url: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.wait_for_load_state("load")

            await page.screenshot(path="antes_screenshot.png")
            try:
                await page.wait_for_selector('text=Deny', state='visible', timeout=5000)
                await page.click('text=Deny')
                print("Botón 'Deny' clickeado exitosamente.")
                await page.screenshot(path="clicked_screenshot.png")
            except Exception as e:
                print(f"No se pudo clickear el botón 'Deny': {e}")
                await page.screenshot(path="error_click_screenshot.png")

            self.content = await page.content()
            #print(self.content)

            await browser.close()

class MetaTag:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

class Form:
    def __init__(self, id: str, action: str, method: str, content: str):
        self.id = id
        self.action = action
        self.method = method
        self.fields = []
        self.content = content

    def add_field(self, field):
        self.fields.append(field)

class Field:
    def __init__(self, name: str, type: str, value: str, content: str):
        self.name = name
        self.type = type
        self.value = value
        self.content = content

class Link:
    def __init__(self, href: str, text: str, rel: str, target: str, content: str):
        self.href = href
        self.text = text
        self.rel = rel
        self.blank = self.is_blank(target)
        self.external = self.is_external(href)
        self.content = content

    def is_blank(self, target: str) -> bool:
        return target and target == "_blank"

    def is_external(self, href: str) -> bool:
        return True
    
class Vulnerability:
    def __init__(self, name: str, type: str, severity: str, location: str, details: str, payload: str = ""):
        self.name = name
        self.type = type
        self.severity = severity
        self.location = location
        self.details = details
        self.payload = payload