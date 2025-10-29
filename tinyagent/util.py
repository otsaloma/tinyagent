# -*- coding: utf-8 -*-

import re

MARKDOWN = """
---
title: {title}
url: {url}
---
{md}
""".strip()

SEPARATOR_LINE = "―" * 72

def _clean_html(html: str) -> str:
    html = re.sub(r"<!--.*?-->", "", html)
    return "\n".join(x for x in html.splitlines() if x.strip())

def _fetch_page(url: str) -> tuple[str, str]:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        browser = playwright.webkit.launch()
        user_agent = playwright.devices["Desktop Safari"]["user_agent"]
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()
        page.goto(url)
        title = page.title()
        html = page.content()
        html = _clean_html(html)
        browser.close()
        return title, html

def fetch_html_as_markdown(url: str) -> str:
    from crawl4ai import DefaultMarkdownGenerator
    title, html = _fetch_page(url)
    generator = DefaultMarkdownGenerator()
    result = generator.generate_markdown(html)
    md = result.raw_markdown.strip()
    return MARKDOWN.format(**locals())

if __name__ == "__main__":
    text = fetch_html_as_markdown("https://example.com/")
    print(text)
    print(len(text))
