import scrapy


class SpiderNameSpider(scrapy.Spider):
    name = "spider_name"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass
