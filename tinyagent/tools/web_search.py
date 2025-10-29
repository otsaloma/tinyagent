# -*- coding: utf-8 -*-

import urllib.parse

from pydantic import Field
from tinyagent import Signature
from tinyagent import Tool
from tinyagent import util

def search(query: str, region: str|None = None) -> str:
    query = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={query}"
    url += f"&kl={region}" if region else ""
    return util.fetch_html_as_markdown(url)

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
