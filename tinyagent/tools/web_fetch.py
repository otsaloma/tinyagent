# -*- coding: utf-8 -*-

from pydantic import Field
from tinyagent import Signature
from tinyagent import Tool
from tinyagent import util

def fetch(url: str) -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.webkit.launch()
        user_agent = p.devices["Desktop Safari"]["user_agent"]
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()
        page.goto(url)
        html = page.content()
        html = util.clean_html(html)
        browser.close()
        return html

class WebFetchSignature(Signature):
    url: str = Field(..., description="URL of web page to fetch")

class WebFetchTool(Tool):
    name = "Fetch web page"
    description = "Use a headless browser to fetch the content of a web page"
    function = fetch
    signature = WebFetchSignature

if __name__ == "__main__":
    tool = WebFetchTool()
    print(tool.schema_json)
    html = tool.call(url="https://example.com/")
    print(html)
