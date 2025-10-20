# -*- coding: utf-8 -*-

import tinyagent as a

from pydantic import Field

def fetch(url: str) -> str:
    return a.util.fetch_html_as_markdown(url)

class WebFetchSignature(a.Signature):
    url: str = Field(..., description="URL of web page to fetch")

class WebFetchTool(a.Tool):
    name = "Fetch web page"
    description = "Use a headless browser to fetch the content of a web page"
    function = fetch
    signature = WebFetchSignature

if __name__ == "__main__":
    tool = WebFetchTool()
    print(tool.schema_json)
    html = tool.call(url="https://example.com/")
    print(html)
