# -*- coding: utf-8 -*-

import tinyagent as a
import urllib.parse

from pydantic import Field

def search(query: str) -> str:
    query = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={query}"
    return a.util.fetch_html_as_markdown(url)

class WebSearchSignature(a.Signature):
    query: str = Field(..., description="Query to search for")

class WebSearchTool(a.Tool):
    name = "Search the internet"
    description = "Use DuckDuckGo to search the internet for a query"
    function = search
    signature = WebSearchSignature

if __name__ == "__main__":
    tool = WebSearchTool()
    print(tool.schema_json)
    html = tool.call(query="Mont Analogue")
    print(html)
