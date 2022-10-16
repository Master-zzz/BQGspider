import requests
from lxml import etree
import random
import csv
from url_info import url_list


class QSspider(object):
    def __init__(self):
        self.url = 'http://www.qibookw.com/book/7/7326/'  # 目录网址
        self.url2 = 'http://www.qibookw.com/'  # 章节网址前半
        self.headers = {'User-Agent': random.choice(url_list)}
        self.writer = {}  # 作者
        self.name = {}  # 书名
        # 创建章节计数器
        self.number = 0

    def save_html(self):  # 提取目录及各章节网址
        html = requests.get(url=self.url, headers=self.headers)
        html.encoding = "gb2312"
        html = html.text
        parse_html = etree.HTML(html)
        dd_list = parse_html.xpath('//div[@class="article_listtext"]/ul/li')
        book_name = parse_html.xpath('//div[@class="book_news_style_text2"]')
        m = 1
        w = 1
        for name in book_name:
            if m == 1:
                self.name = name.xpath('.//h1/text()')[0].strip()
                m = m+1
            else:
                break
        for writer in book_name:
            if w == 1:
                self.writer = writer.xpath('.//p/text()')[0].strip()
                w = w+1
            else:
                break
        item = {}
        with open('mulu2.csv', 'w', newline='', encoding="utf-8") as f:
            fieldname = ['title', 'url']
            writer = csv.DictWriter(f, fieldnames=fieldname)
            writer.writeheader()
            for dd in dd_list:
                item['title'] = dd.xpath('.//a/text()')[0].strip()
                item['url'] = dd.xpath('.//a/@href')[0].strip()
                writer.writerow(item)

    def catch(self):
        with open('mulu2.csv', 'r', newline='', encoding="utf-8") as m:
            lite = csv.DictReader(m)
            for row in lite:
                title = row['title']
                yurl = str(self.url2) + str(row['url'])
                htmll = requests.get(url=yurl, headers=self.headers)
                htmll.encoding = "gb2312"
                htmll = htmll.text
                parse_html2 = etree.HTML(htmll)
                pageall_list = parse_html2.xpath('//div[@class="novel_content"]/br')
                first_text = parse_html2.xpath('//div[@class="novel_content"]')[0].text.strip()
                file = open(r'A:\Pycharm\project\spider\ ' + str(self.name) + ' ' + str(self.writer) + '.txt', 'a+', encoding='utf-8')
                file.write('\n' + title)
                file.write('\n' + first_text.strip())
                for u in pageall_list:
                    file.write('\n' + u.tail.strip())
                self.number = self.number + 1
                print(self.number)

    def run(self):
        self.save_html()
        self.catch()


if __name__ == '__main__':
    spider = QSspider()
    spider.run()
