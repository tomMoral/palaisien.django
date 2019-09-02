import re
import traceback
from django.shortcuts import render

from .models import Talk


def process_code_blocks(text):
    codes = re.findall(r'`[^`]*`', text)
    for c in codes:
        code_block = '<span class="highlightcode">' + c[1:-1]
        code_block += '</span>'
        text = text.replace(c, code_block)
    text = text.replace("\n", "</br>\n")
    return text


def index(request):
    latest_talk_list = Talk.objects.order_by('-pub_date')

    for t in latest_talk_list:
        t.title = process_code_blocks(t.title)
        t.short_description = process_code_blocks(t.short_description)
        t.abstract = process_code_blocks(t.abstract)

    context = {
        'talks': latest_talk_list,
        'content': "programme/{}.html".format(request.path[1:]),
    }
    print(context)
    try:
        res = render(request, 'programme/index.html', context)
    except Exception as e:
        traceback.print_exc()
        context["content"] = "programme/about.html"
        res = render(request, 'programme/index.html', context)

    return res
