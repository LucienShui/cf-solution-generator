#!/usr/bin/env python3
import requests
from sys import argv
from bs4 import BeautifulSoup


template = """# {{ title }}

## 地址

{{ url }}

## 原文地址

{{ blog }}

## 题目

{{ content }}

## 题意



## 题解



### 代码

{{ pasteme }}

```cpp
{{ code }}
```

"""


replace = {
    "component": {
        "</p>": "",
        "<p>": "",
        "$$$": "$",
    },
    "font_type": {
        "tex-font-style-bf": "**",
        "tex-font-style-tt": "`",
    }
}


def error(*args):
    print(*args)
    exit(0)


def render(tmp, __body):
    for i in __body:
        tmp = tmp.replace("{{ %s }}" % i, __body[i])
    return tmp


def post(code):
    return requests.api.post("https://pasteme.cn/api/set.php", data={
        "content": code,
        "type": "cpp",
    }).json()["keyword"]


if __name__ == "__main__":
    if argv.__len__() != 4:
        error("Usage: gen <contest id> <problem id> <archive id>")

    file_content = open("%s.cpp" % argv[2].lower()).read().replace("\t", "    ")
    body = {
        "url": "http://codeforces.com/contest/%s/problem/%s" % (argv[1], argv[2].upper()),
        "code": file_content,
        "pasteme": "https://pasteme.cn/%s" % post(file_content),
        "blog": "https://www.lucien.ink/archives/%s" % argv[3],
    }
    html = requests.api.get(body["url"]).text
    html = BeautifulSoup(html, features="lxml")
    title = html.find_all(class_="title")[0].string.split(". ")[1]
    body["title"] = "Codeforces - %s%s - %s" % (argv[1], argv[2].upper(), title)
    content = html.find(class_="problem-statement")
    content = content.find_all(name="div")[10]

    span_list = content.find_all(name="span")
    for each in span_list:
        class_name = each["class"]
        if class_name.__len__() > 1:
            error("More than one class", str(each))
        class_name = class_name[0]
        if class_name not in replace["font_type"]:
            error("No such class", str(each))

        replace["component"][str(each)] = replace["font_type"][
                                              class_name] + each.string + replace["font_type"][class_name]

    content = content.find_all(name="p")
    output = ""
    for line in map(str, content):
        for each in replace["component"]:
            line = line.replace(each, replace["component"][each])
        output = "%s%s\n\n" % (output, line)

    body["content"] = output

    with open("%s.md" % body["title"], "w") as file:
        file.write(render(template, body))

