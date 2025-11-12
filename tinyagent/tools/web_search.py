# -*- coding: utf-8 -*-

import urllib.parse

from bs4 import BeautifulSoup
from pydantic import Field
from tinyagent import Signature
from tinyagent import Tool
from tinyagent import util

def search(query: str, region: str|None = None) -> str:
    query = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={query}"
    url += f"&kl={region}" if region else ""
    title, html = util.fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.select("#header"): tag.decompose()
    for tag in soup.select(".result--ad"): tag.decompose()
    return util.html_to_markdown(url, title, str(soup))

class WebSearchSignature(Signature):
    query: str = Field(..., description="Query to search for")

class WebSearchTool(Tool):
    name = "web_search"
    description = "Use DuckDuckGo to search the internet for a query"
    function = search
    signature = WebSearchSignature

    def __init__(self, *, region: str|None = None):
        # For valid region values, see 'kl' in the documentation.
        # https://duckduckgo.com/duckduckgo-help-pages/settings/params
        super().__init__()
        self.extra_kwargs["region"] = region

if __name__ == "__main__":
    tool = WebSearchTool(region="fr-fr")
    print(tool.schema_json)
    text = tool.call(query="Mont Analogue")
    print(text)
    print(len(text))
