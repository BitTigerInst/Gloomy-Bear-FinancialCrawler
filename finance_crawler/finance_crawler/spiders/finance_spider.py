import scrapy
import re
from scrapy.selector import Selector
from finance_crawler.items import FinanceCrawlerItem

class RetuersSpider(scrapy.Spider):
    name = "retuers"
    allowed_domains = ["reuters.com"]
    url_base = "http://blogs.reuters.com/breakingviews/page/"  
    start_urls=[url_base + str(x) + "/" for x in range(1,587)]
    def parse(self, response):
        page = Selector(response)
        hrefs = page.xpath('.//h2/a/@href')
        for href in hrefs:
            url = href.extract()
            yield scrapy.Request(url, callback = self.parse_item)
   
    def parse_item(self, response):
        page = Selector(response)
        item = FinanceCrawlerItem()
        item['title'] = response.xpath('//div[@class="columnRight grid8"]/h2/text()').extract();
        item['url'] = response.url
        item['author'] = response.xpath('//div[@class="author"]/text()').extract()
        item['timeStamp'] = response.xpath('.//div[@class="timestamp"]/text()').extract()
        item['content'] = response.xpath('.//div[@id="postcontent"]/p/text()').extract()
        yield item
          
