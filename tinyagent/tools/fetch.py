# -*- coding: utf-8 -*-

from pydantic import Field
from tinyagent import Signature
from tinyagent import Tool

def fetch(url: str) -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()
        return html

class FetchSignature(Signature):
    url: str = Field(..., description="URL of web page to fetch")

class FetchTool(Tool):
    name = "Fetch web page"
    description = "Use a headless browser to fetch the content of a web page"
    function = fetch
    signature = FetchSignature

if __name__ == "__main__":
    tool = FetchTool()
    print(tool.schema_json)
    html = tool.call(url="https://example.com/")
    print(html)
