import json
import argparse
import requests

from io import StringIO
from lxml import etree


def download_site(url):
    return requests.get(url).text


def parse_response(url, text):
    htmlparser = etree.HTMLParser()
    tree = etree.parse(StringIO(text), htmlparser)

    forms = []

    for form in tree.xpath('//form'):
        attrs = form.attrib

        data = {
            'action': url,
            'method': 'POST',
            'name': None,
            'parameters': []
        }

        if 'action' in attrs and len(attrs['action']) > 0:
            data['action'] = attrs['action']

        if 'method' in attrs and len(attrs['method']) > 0:
            data['method'] = attrs['method'].upper()

        if 'name' in attrs and len(attrs['name']) > 0:
            data['name'] = attrs['name']

        for param in form.xpath('.//*[@name]'):
            parameter = {
                'name': None,
                'value': None
            }

            if 'name' in param.attrib and len(param.attrib['name']) > 0:
                parameter['name'] = param.attrib['name']

            if 'value' in param.attrib and len(param.attrib['value']) > 0:
                parameter['value'] = param.attrib['value']

            data['parameters'].append(parameter)

        forms.append(data)

    return forms


def get_forms(url):
    data = download_site(url)

    return parse_response(url, data)


def main():
    parser = argparse.ArgumentParser(description='Form extractor')
    parser.add_argument('url', type=str, help='Target url')

    args = parser.parse_args()

    url = args.url

    data = {
        'url': url,
        'forms': get_forms(url)
    }

    print(json.dumps(data))


if __name__ == "__main__":
    main()
