# -*- coding: utf-8 -*-

import re

def clean_html(html: str) -> str:
    out = []
    for line in html.splitlines():
        line = re.sub(r"<!--.*?-->", "", line)
        if line := line.strip():
            out.append(line)
    return "\n".join(out)
