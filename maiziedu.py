# --coding: utf-8 --

from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

time1 = time.time()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'}


class Maiziedu(object):

    def link(self, url):
        page = requests.get(url, headers=headers)
        html = etree.HTML(page.text)
        selector = html.xpath('//ul[@class="zy_course_list"]')
        for each in selector:
            page_url = each.xpath('li/a/@href')
            for link in page_url:
                link = r'http://www.maiziedu.com' + link
                # time.sleep(3)
                self.Content(link)

    def Content(self, url):
        page = requests.get(url, headers=headers)
        html = etree.HTML(page.text)
        selector = html.xpath('//*[@id="playlist"]')
        for each in selector:
            page_url = each.xpath('ul/li/a/@href')
            for link in page_url:
                link = r'http://www.maiziedu.com' + link
                self.Section(link)

    def Section(self, url):
        page = requests.get(url, headers=headers)
        html = etree.HTML(page.text)
        title = html.xpath('//div[@class="course-play"]/dl/dt/text()')[0].replace('\t', '').replace('\\', '&')
        self.title = ''.join(title).decode('utf-8')
        selector = html.xpath('//div[@class="course-play"]')
        item = {}
        for each in selector:
            section = each.xpath('.//a[@class="active"]/text()')
            download_url = each.xpath('.//video[@id="microohvideo"]/source/@src')
            print ''.join(section).decode('utf-8')
            print ''.join(download_url).decode('utf-8')
            item['section'] = ''.join(section).decode('utf-8')
            item['download_url'] = ''.join(download_url).decode('utf-8')
            self.towrite(item)

    def towrite(self, contentdict):
        filename = r'd:/maiziedu/%s.txt' % self.title
        f = open(filename, 'a')
        f.writelines(u'章节名称:' + contentdict['section'] + '\n')
        f.writelines(u'下载连接:' + contentdict['download_url'] + '\n\n')
        f.close

    def main(self):
        pool = ThreadPool(1)
        page = []
        for i in range(1, 23):
            index_url = r'http://www.maiziedu.com/course/list/?catagory=all&career=all&sort_by=&page=' + \
                str(i)
            page.append(index_url)

        result = pool.map(self.link, page)
        pool.close()
        pool.join()


if __name__ == '__main__':
    s = Maiziedu()
    s.main()

time2 = time.time()
print time2 - time1
