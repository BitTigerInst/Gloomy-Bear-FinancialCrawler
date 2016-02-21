import scrapy
import re
from scrapy.selector import Selector
from finance_crawler.items import FinanceCrawlerItem

class RetuersSpider(scrapy.Spider):
    name = "retuers"
    allowed_domains = ["reuters.com"]
    url_base = "http://blogs.reuters.com/breakingviews/page/"  
    start_urls=[url_base + str(x) + "/" for x in range(1,587)]
    # start_urls=[url_base + str(1)]
    def parse(self, response):
        page = Selector(response)
        hrefs = page.xpath('.//h2/a/@href')
        for href in hrefs:
            url = href.extract()
            yield scrapy.Request(url, callback = self.parse_item)
   
    def parse_item(self, response):
        page = Selector(response)
        item = FinanceCrawlerItem()

        mores = response.xpath('//h3/a/@href')
        # mores = response.xpath('//li[id="rsspie-4"]/a/@href')
        for more in mores:
            url = more.extract()
            if "video" not in url:
                yield scrapy.Request(url, callback = self.parse_news_page)
        item['title'] = response.xpath('//div[@class="columnRight grid8"]/h2/text()').extract();
        item['url'] = response.url
        item['author'] = response.xpath('//div[@class="author"]/text()').extract()
        item['timeStamp'] = response.xpath('.//div[@class="timestamp"]/text()').extract()
        item['content'] = response.xpath('.//div[@id="postcontent"]/p/text()').extract()
        yield item

    def parse_news_page(self, response):
        page = Selector(response)
        item = FinanceCrawlerItem()
        title = response.xpath('//h1[@class="article-headline"]/text()').extract()
        paragraphs = response.xpath('//span[@id="articleText"]/p/text()').extract()
        content = ""

        for paragraph in paragraphs:
            content += paragraph

        if title:
            url = response.url
            #remove useless arguments
            if "?" in url:
                index = url.index('?')
                url = url[0:index]
            item['title'] = title
            item['url'] = url
            item['author'] = response.xpath('//span[@class="byline"]/a/text()').extract()
            item['timeStamp'] = response.xpath('//span[@class="timestamp"]/text()').extract()
            item['content'] = content.encode('utf-8')
            yield item


          
