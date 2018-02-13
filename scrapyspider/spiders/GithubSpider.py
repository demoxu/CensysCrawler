from scrapy.spiders import Spider
from scrapyspider.items import PhpStudyItem
from scrapy.http import Request
from scrapy.http import FormRequest

class GithubSpider(Spider):
    name = 'github'

    start_urls = ['https://www.censys.io/ipv4/_search?q=phpStudy']


    def parse(self, response):
        print(1)