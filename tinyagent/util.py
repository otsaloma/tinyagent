# -*- coding: utf-8 -*-

import re

def clean_html(html: str) -> str:
    out = []
    for line in html.splitlines():
        line = re.sub(r"<!--.*?-->", "", line)
        if line := line.strip():
            out.append(line)
    return "\n".join(out)

def fetch_html(url: str) -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.webkit.launch()
        user_agent = p.devices["Desktop Safari"]["user_agent"]
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()
        page.goto(url)
        html = page.content()
        html = clean_html(html)
        return html

def fetch_html_as_markdown(url: str) -> str:
    from crawl4ai import DefaultMarkdownGenerator
    html = fetch_html(url)
    generator = DefaultMarkdownGenerator()
    result = generator.generate_markdown(html)
    return result.raw_markdown
