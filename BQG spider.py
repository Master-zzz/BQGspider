import requests
from lxml import etree
import random
import csv
import time
from ua_info import ua_list


class MaoyanSpider(object):
    def __init__(self):
        self.url = 'https://www.1bqg.net/1bqg/851459570/'  # 目录网址
        self.url2 = 'https://www.1bqg.net'  # 章节网址前半
        self.headers = {'User-Agent': random.choice(ua_list)}
        # 创建章节计数器
        self.number = 0

    def save_html(self):  # 提取目录及各章节网址
        html = requests.get(url=self.url, headers=self.headers).text
        parse_html = etree.HTML(html)
        dd_list = parse_html.xpath('//div[@class="box_con"]/dl/dd')
        dd_list = dd_list[12:]
        item = {}
        with open('mulu.csv', 'w', newline='') as f:
            fieldname = ['title', 'url']
            writer = csv.DictWriter(f, fieldnames=fieldname)
            writer.writeheader()
            for dd in dd_list:
                item['title'] = dd.xpath('.//a/text()')[0].strip()
                item['url'] = dd.xpath('.//a/@href')[0].strip()
                writer.writerow(item)
                # time.sleep(random.randint(2, 3))  # 延迟时间

    def catch(self):
        with open('mulu.csv', 'r', newline='') as m:
            lite = csv.DictReader(m)
            for row in lite:
                # 解析错误时跳过部分章节处理器#
                # if self.number == 124 or self.number == 125 or self.number == 126 or self.number == 127:
                #     self.number = self.number + 1
                #     continue
                title = row['title']
                yurl = str(self.url2) + str(row['url'])
                htmll = requests.get(url=yurl, headers=self.headers)
                try:
                    html2 = htmll.content.decode('gbk').encode('gbk')
                except:
                    htmll.decode = 'gb18030'
                    htmll.encoding = 'gb18030'
                    html2 = htmll.text
                parse_html2 = etree.HTML(html2)
                pd = parse_html2.xpath('//div[@id="content"]/p')
                if pd:
                    d_list = parse_html2.xpath('//div[@id="content"]/p')
                    pageall = len(parse_html2.xpath('//div[@id="PageSet"]/a'))  # 判断是否有下一页
                    file = open(r'A:\Pycharm\project\spider\逍遥小都督.txt', 'a+', encoding='utf-8')
                    file.write('\n' + title)
                    for d in d_list:
                        try:
                            text = d.xpath('.//text()')[0].strip()
                            file.write('\n' + text)
                        except:
                            continue
                    if pageall != 0:
                        for n in range(pageall - 1):
                            url = yurl[:-5]
                            url = url + '-' + str(n + 2) + '.html'
                            html3 = requests.get(url=url, headers=self.headers)
                            try:
                                html3 = html3.content.decode('gbk').encode('gbk')
                            except:
                                html3.decode = 'gb18030'
                                html3.encoding = 'gb18030'
                                html3 = htmll.text
                            parse_html3 = etree.HTML(html3)
                            d_list2 = parse_html3.xpath('//div[@id="content"]/p')
                            for D in d_list2:
                                try:
                                    text1 = D.xpath('.//text()')[0].strip()
                                    file.write('\n' + text1)
                                except:
                                    continue
                    file.close()
                else:
                    first_text = parse_html2.xpath('//div[@id="content"]')[0].text.strip()
                    pageall = len(parse_html2.xpath('//div[@id="PageSet"]/a'))
                    ddd_list = parse_html2.xpath('//div[@id="content"]/br')
                    file = open(r'A:\Pycharm\project\spider\逍遥小都督.txt', 'a+', encoding='utf-8')
                    file.write('\n' + title)
                    try:
                        file.write('\n' + first_text.strip())
                    except:
                        pass
                    for u in ddd_list:
                        try:
                            file.write('\n' + u.tail.strip())
                        except:
                            continue
                    if pageall != 0:
                        for n in range(pageall - 1):
                            url = yurl[:-5]
                            url = url + '-' + str(n + 2) + '.html'
                            html3 = requests.get(url=url, headers=self.headers)
                            try:
                                html3 = html3.content.decode('gbk').encode('gbk')
                            except:
                                html3.decode = 'gb18030'
                                html3.encoding = 'gb18030'
                                html3 = htmll.text
                            parse_html3 = etree.HTML(html3)
                            ddd_list2 = parse_html3.xpath('//div[@id="content"]/br')
                            for Dd in ddd_list2:
                                try:
                                    file.write('\n' + Dd.tail.strip())
                                except:
                                    continue
                    file.close()
                self.number = self.number + 1
            # time.sleep(random.randint(2, 3))  # 延迟时间

    def run(self):
        self.save_html()
        self.catch()


if __name__ == '__main__':
    spider = MaoyanSpider()
    spider.run()
