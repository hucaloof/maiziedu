# --coding: utf-8 --

from lxml import etree
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Link(object):

    def __init__(self):
        pass

    def link(self, url):
        page = requests.get(url)
        html = etree.HTML(page.text)
        selector = html.xpath('//ul[@class="zy_course_list"]')
        infolist = []
        for each in selector:
            info = {}
            info['page_url'] = each.xpath('li/a/@href')
            infolist.append(info)
        return infolist


def main():
    links = []
    for i in range(1, 23):
        index_url = r'http://www.maiziedu.com/course/list/?catagory=all&career=all&sort_by=&page=' + str(i)
        result = Link().link(index_url)
        for r in result:
            for page_url in r['page_url']:
                link = 'http://www.maiziedu.com' + page_url
                links.append(link)
    return links

if __name__ == '__main__':
    main()
