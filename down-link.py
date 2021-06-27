import httpx
from urllib import parse
import os

def get_pdf_content(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59"
    }
    resp = httpx.get(url, headers=headers)
    return resp.content


def save_pdf(location, link):
    if not os.path.exists(location):
        pardir = os.path.dirname(location)
        if not os.path.exists(pardir):
            os.mkdir(pardir)
        content = get_pdf_content(link)
        with open(location, 'wb') as fp:
            fp.write(content)


def get_items(url):
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59"
    }
    r = httpx.get(url, headers=headers)
    items = r.json()
    return items

root_url = ''

def parse_data(url, prefix='./pdf'):
    for index, item in enumerate(get_items(url)):
        text = item.get('text')
        href = item.get('href')
        location = f'{prefix}/{str(index+1).zfill(2)}.{text}'
        pageLink = parse.urljoin(root_url, href)
        pageId = item.get('pageId')
        pdf_link = parse.urljoin(root_url, f'/spaces/flyingpdf/pdfpageexport.action?pageId={pageId}')
        pdf_location = f'{location}.pdf'
        print(pdf_location, pdf_link)
        save_pdf(pdf_location, pdf_link)
        if item.get('nodeClass') == 'closed undraggable':
            children_url = parse.urljoin(root_url, f'/pages/children.action?pageId={pageId}')
            parse_data(children_url, prefix=location)


def main():
    url = parse.urljoin(root_url, '/pages/children.action?spaceKey=kaiyang&node=root')
    parse_data(url)



if __name__ == '__main__':
    main()