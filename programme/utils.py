
import re


def process_code_blocks(text):
    codes = re.findall(r'`[^`]*`', text)
    for c in codes:
        code_block = '<span class="highlightcode">' + c[1:-1]
        code_block += '</span>'
        text = text.replace(c, code_block)
    text = text.replace("\n", "</br>\n")
    return text
