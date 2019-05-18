#!/usr/bin/env python3
import requests
from sys import argv
from bs4 import BeautifulSoup

replace = {
    "component": {
        "</p>": "",
        "<p>": "",
        "$$$": "$",
    },
    "font_type": {
        "tex-font-style-bf": "**",
        "tex-font-style-tt": '`',
    }
}

if __name__ == '__main__':
    if argv.__len__() != 4:
        print('Usage: gen <contest id> <problem id> <archive id>')
        exit(0)

    html = requests.api.get('http://codeforces.com/contest/%s/problem/%s' % (argv[1], argv[2])).text
    html = BeautifulSoup(html, features="lxml")
    title = html.find_all(class_='title')[0].string.split('. ')[1]
    print('Title: Codeforces - %s%s - %s' % (argv[1], argv[2], title))
    content = html.find(class_='problem-statement')
    content = content.find_all(name='div')[10]

    span_list = content.find_all(name='span')
    for each in span_list:
        class_name = each['class']
        if class_name.__len__() > 1:
            print('More than one class', str(each))
            exit(0)
        class_name = class_name[0]
        if class_name not in replace['font_type']:
            print('No such class', str(each))
            exit(0)
        replace['component'][str(each)] = replace['font_type'][
                                              class_name] + each.string + replace['font_type'][class_name]

    content = content.find_all(name='p')
    for line in map(str, content):
        for each in replace['component']:
            line = line.replace(each, replace['component'][each])
        print(line, end='\n\n')
        
