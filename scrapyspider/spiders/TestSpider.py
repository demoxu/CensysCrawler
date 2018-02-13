from scrapy.spiders import Spider
from scrapyspider.items import PhpStudyItem
from scrapy.http import Request
from scrapy.http import FormRequest
import time

class TestSpider(Spider):

    name = 'testspider'

    handle_httpstatus_list = [403,404,429]

    headers = {
        'accept': 'image/webp,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.8',
        'referer': 'https://www.censys.io/',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    }

    Page = 1
    MaxPage = 511

    url = 'https://www.censys.io/ipv4/_search?q=phpStudy&page='

    def start_requests(self):
         return [Request("https://www.censys.io/login",meta={'cookiejar': 1},dont_filter=True,callback=self.post_login)]

    def post_login(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').extract()[0]
        came_from = response.xpath('//input[@name="came_from"]/@value').extract()[0]
        print(csrf_token)
        print(came_from)
        return [FormRequest.from_response(response,
                                          url='https://www.censys.io/login',
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          method='POST',
                                          headers=self.headers,
                                          formdata={
                                              'csrf_token': csrf_token,
                                              'came_from' : came_from,
                                              'login': '443741054@qq.com',
                                              'password': 'a8621121'
                                          },
                                          callback=self.after_login,
                                          dont_filter=True
                                          )]

    def after_login(self, response) :
        url  = self.url + str(self.Page)
        yield Request(url, meta={'cookiejar': response.meta['cookiejar']})

    def parse(self, response):
        if response.status == 429:
            time.sleep(200)
            next_url = self.url + str(self.Page)
            yield Request(next_url,meta={'cookiejar': True},dont_filter=True, headers=self.headers)
        else:
            item = PhpStudyItem()
            servers = response.xpath('//div[@class="result"]')

            print(servers)

            with open('1.txt', 'a') as f:
                 for server in servers:
                      f.write('\n' + str.strip(server.xpath('.//span[@class="ip"]/a/text()').extract()[0].replace("\n", "")) + '/phpmyadmin')
                        # item['path'] = server.xpath('.//div[@class="results-hightlight"]/b/text()').extract()[0] + ':' +server.xpath('.//div[@class="results-hightlight"]/tt/mark/text()').extract()[0] + server.xpath('.//div[@class="results-hightlight"]/tt/text()').extract()[0]
                        # item['port'] = server.xpath('.//div[@class="results-metadata"]/span[4]/text()').extract()[0]

            self.Page += 1
            next_url = self.url + str(self.Page)

            if self.Page <= self.MaxPage:
                yield Request(next_url,meta={'cookiejar': True},dont_filter=True, headers=self.headers)
