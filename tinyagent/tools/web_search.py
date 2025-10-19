# -*- coding: utf-8 -*-

import urllib.parse

from pydantic import Field
from tinyagent import Signature
from tinyagent import Tool
from tinyagent import util

def search(query: str) -> str:
    from playwright.sync_api import sync_playwright
    query = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={query}"
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

class WebSearchSignature(Signature):
    query: str = Field(..., description="Query to search for")

class WebSearchTool(Tool):
    name = "Search the internet"
    description = "Use DuckDuckGo to search the internet for a query"
    function = search
    signature = WebSearchSignature

if __name__ == "__main__":
    tool = WebSearchTool()
    print(tool.schema_json)
    html = tool.call(query="When will AI destroy humanity?")
    print(html)
