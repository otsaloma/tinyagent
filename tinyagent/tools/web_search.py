# -*- coding: utf-8 -*-

import urllib.parse

from pydantic import Field
from tinyagent import Signature
from tinyagent import Tool
from tinyagent import util

def search(query: str) -> str:
    query = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={query}"
    return util.fetch_html_as_markdown(url)

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
    text = tool.call(query="Mont Analogue")
    print(text)
    print(len(text))
