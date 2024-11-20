import json
import os
import time

import requests
from bs4 import BeautifulSoup
#功能
#根据数量爬取网站上文章的数量
#爬取每个网址文章的内容
#将文章存取到本地数据 若存在则不再爬取 直接读取本地文件 -----额外功能

#https://ctext.org/hongloumeng/ch1



headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
}



class web_crawler:

    def __init__(self,web_number:int):
        self.content_dict=dict()
        self.web_number=web_number

    def get_url(self,number: int) -> list:
        url_list = list()
        for num in range(0, number):
            url_list.append(f"https://ctext.org/rulin-waishi/{str(num + 1)}")
        return url_list

    # Web Crawling
    def get_content(self,url: str):

        data = ''

        with requests.get(url,headers=headers) as response:
            if response.status_code == 200:
                # 解析 HTML 内容
                soup = BeautifulSoup(response.text, 'html.parser')

                # 找到包含文本的元素
                # 这里假设我们要提取所有的段落（<td>标签）
                paragraphs = soup.find_all('td', class_='ctext')

                # 提取并打印文本内容
                for p in paragraphs:
                    data += p.get_text(strip=True) + '\n'  # 使用 += 来累加文本内容
                return data
            else:
                print(f"请求失败，状态码：{response.status_code}")

    def get_all_chapter_content(self):
        counter=1
        for url in self.get_url(self.web_number):
            print(url)
            time.sleep(1)
            result=self.get_content(url)
            self.content_dict[f"{str(counter)}"]=result

            with open(f"{counter}.txt", 'w', encoding='utf-8') as file:
                file.write(result)#save all the crawled data to the local system
            counter+=1






if __name__=="__main__":

    crawler=web_crawler(20)#Select the number of chapters to crawl

    crawler.get_all_chapter_content()#start to crawl the data from the webpages






