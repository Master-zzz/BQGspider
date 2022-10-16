import requests
from lxml import etree
import random
import csv
from url_info import url_list


class BQSpider(object):
    def __init__(self):
        self.url = 'https://www.1bqg.net/1bqg/881205935/'  # 目录网址
        self.url2 = 'https://www.1bqg.net'  # 章节网址前半
        self.headers = {'User-Agent': random.choice(url_list)}
        self.name = {}  # 书名
        self.writer = {}  # 作者
        self.number = 0  # 创建章节计数器

    def save_html(self):  # 提取目录及各章节网址
        html = requests.get(url=self.url, headers=self.headers)
        html.encoding = "gb2312"
        html = html.text
        parse_html = etree.HTML(html)
        dd_list = parse_html.xpath('//div[@class="box_con"]/dl/dd')
        book_name = parse_html.xpath('//div[@id="info"]')
        n = 1
        w = 1
        for name in book_name:
            if n == 1:
                self.name = name.xpath('.//h1/text()')[0].strip()
                n = n+1
            else:
                break
        for writer in book_name:
            if w == 1:
                self.writer = writer.xpath('.//p/text()')[0].strip()
                w = w+1
            else:
                break
        dd_list = dd_list[12:]
        item = {}
        with open('mulu.csv', 'w', newline='', encoding="utf-8") as f:
            fieldname = ['title', 'url']
            writer = csv.DictWriter(f, fieldnames=fieldname)
            writer.writeheader()
            for dd in dd_list:
                item['title'] = dd.xpath('.//a/text()')[0].strip()
                item['url'] = dd.xpath('.//a/@href')[0].strip()
                writer.writerow(item)

    def catch(self):
        with open('mulu.csv', 'r', newline='', encoding="utf-8") as m:
            lite = csv.DictReader(m)
            for row in lite:
                # 解析错误时跳过部分章节处理器#
                # if self.number == 124 or self.number == 125 or self.number == 126 or self.number == 127:
                #     self.number = self.number + 1
                #     continue
                title = row['title']
                yurl = str(self.url2) + str(row['url'])
                htmll = requests.get(url=yurl, headers=self.headers)
                htmll.encoding = "gb2312"
                html2 = htmll.text
                parse_html2 = etree.HTML(html2)
                pd = parse_html2.xpath('//div[@id="content"]/p')
                if pd:
                    d_list = parse_html2.xpath('//div[@id="content"]/p')
                    pageall = len(parse_html2.xpath('//div[@id="PageSet"]/a'))  # 判断是否有下一页
                    file = open(r'A:\Pycharm\project\spider\ ' + str(self.name) + ' ' + str(self.writer) + '.txt', 'a+', encoding='utf-8')
                    file.write('\n' + title)
                    for d in d_list:
                        text = d.xpath('.//text()')[0].strip()
                        file.write('\n' + text)
                    if pageall != 0:
                        for n in range(pageall - 1):
                            url = yurl[:-5]
                            url = url + '-' + str(n + 2) + '.html'
                            html3 = requests.get(url=url, headers=self.headers)
                            html3.encoding = "gb2312"
                            html3 = html3.text
                            parse_html3 = etree.HTML(html3)
                            d_list2 = parse_html3.xpath('//div[@id="content"]/p')
                            for D in d_list2:
                                text1 = D.xpath('.//text()')[0].strip()
                                file.write('\n' + text1)
                    file.close()
                else:
                    first_text = parse_html2.xpath('//div[@id="content"]')[0].text
                    pageall = len(parse_html2.xpath('//div[@id="PageSet"]/a'))
                    ddd_list = parse_html2.xpath('//div[@id="content"]/br')
                    file = open(r'A:\Pycharm\project\spider\ ' + str(self.name) + ' ' + str(self.writer) + '.txt', 'a+', encoding='utf-8')
                    file.write('\n' + title)
                    if not first_text:
                        pass
                    else:
                        file.write('\n' + first_text.strip())
                    for u in ddd_list:
                        if not u.tail:
                            pass
                        else:
                            file.write('\n' + u.tail.strip())
                    if pageall != 0:
                        for n in range(pageall - 1):
                            url = yurl[:-5]
                            url = url + '-' + str(n + 2) + '.html'
                            html3 = requests.get(url=url, headers=self.headers)
                            html3.encoding = "gb2312"
                            html3 = html3.text
                            parse_html3 = etree.HTML(html3)
                            ddd_list2 = parse_html3.xpath('//div[@id="content"]/br')
                            for Dd in ddd_list2:
                                if not Dd.tail:
                                    pass
                                else:
                                    file.write('\n' + Dd.tail.strip())
                    file.close()
                self.number = self.number + 1
                print(self.number)

    def run(self):
        self.save_html()
        self.catch()


if __name__ == '__main__':
    spider = BQSpider()
    spider.run()
