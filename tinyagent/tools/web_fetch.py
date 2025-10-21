# -*- coding: utf-8 -*-

from pydantic import Field
from tinyagent import Signature
from tinyagent import Tool
from tinyagent import util

def fetch(url: str) -> str:
    return util.fetch_html_as_markdown(url)

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
    text = tool.call(url="https://example.com/")
    print(text)
    print(len(text))
