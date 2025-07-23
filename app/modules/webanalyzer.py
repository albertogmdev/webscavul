from app.core.webpage import WebPage, MetaTag, Form, Field, Link, Vulnerability

from bs4 import BeautifulSoup

def analyze_webpage(webpage: WebPage):
    print("INFO: Analyzing webpage content")

    analyze_forms(webpage)

def analyze_forms(webpage: WebPage):
    print("INFO: Analyzing forms in the webpage")