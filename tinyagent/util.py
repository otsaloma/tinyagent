# -*- coding: utf-8 -*-

import atexit
import contextlib
import functools
import re

@functools.cache
def get_browser_context():
    from playwright.sync_api import sync_playwright
    playwright = sync_playwright().start()
    browser = playwright.webkit.launch()
    user_agent = playwright.devices["Desktop Safari"]["user_agent"]
    context = browser.new_context(user_agent=user_agent)
    atexit.register(playwright.stop)
    atexit.register(context.close)
    return context

@contextlib.contextmanager
def new_browser_page(url: str):
    context = get_browser_context()
    page = context.new_page()
    page.goto(url)
    yield page
    page.close()

def clean_html(html: str) -> str:
    out = []
    for line in html.splitlines():
        line = re.sub(r"<!--.*?-->", "", line)
        if line := line.strip():
            out.append(line)
    return "\n".join(out)

def fetch_html(url: str) -> str:
    with new_browser_page(url) as page:
        html = page.content()
        html = clean_html(html)
        return html

def fetch_html_as_markdown(url: str) -> str:
    from crawl4ai import DefaultMarkdownGenerator
    html = fetch_html(url)
    generator = DefaultMarkdownGenerator()
    result = generator.generate_markdown(html)
    return result.raw_markdown.strip()

def print_separator_line() -> None:
    print("―" * 72)

if __name__ == "__main__":
    text = fetch_html_as_markdown("https://example.com/")
    print(text)
    print(len(text))
