import scrapy
import os
from ..items import SidexItem


class SidexSpider(scrapy.Spider):
    name = "sidex"
    allowed_domains = ["www.sidex.or.kr"]
    start_urls = ["https://www.sidex.or.kr"]
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapyFW.pipelines.BasicJsonPipeline': 300
        },
    }
    
    def __init__(self, *args, **kwargs):
        super(SidexSpider, self).__init__(*args, **kwargs)
        self.page = 1
        self.crawl_state = True
        self.basic_url = 'https://www.sidex.or.kr/exhibition/partner_search.php?&findType=&findword=&page='
        
        self.pipeline_output_path = os.path.join('results','sidex','sidex.json')
        if not os.path.exists(os.path.dirname(self.pipeline_output_path)):
            os.makedirs(os.path.dirname(self.pipeline_output_path))
            
        self.detail_num = 0
    
    def start_requests(self):
        url = f"{self.basic_url}{self.page}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        links = response.css('#contents > section > div > div.table-responsive > table > tbody > tr a::attr(href)').extract()
        
        amount_of_links = len(links)
        
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_detail)
        # yield scrapy.Request(url=response.urljoin(links[0]), callback=self.parse_detail)
        
        if amount_of_links < 10:
            self.crawl_state = False
        elif amount_of_links == 10:
            self.page += 1
            
        if self.crawl_state:
            url = f"{self.basic_url}{self.page}"
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse_detail(self, response):
        self.detail_num += 1
        print(f"detail number = {self.detail_num}")
        
        booth_number = response.css('#contents > section > div > div:nth-child(1) > div.booth::text').extract()
        if len(booth_number) > 0:
            booth_number = booth_number[1].strip()
        else:
            booth_number = ''
        
        item = SidexItem()
        item['name'] = response.css('#contents > section > div > div:nth-child(1) > h3::text').get('').strip()
        item['hall_number'] = response.css('#contents > section > div > div:nth-child(1) > div.booth > span::text').get('').strip()
        item['booth_number'] = booth_number
        item['address'] = response.css('#contents > section > div > div:nth-child(1) > div.row > div.col-12.col-md-7.flex-grow-1 > div > table > tbody > tr:nth-child(1) > td::text').get('').strip()
        item['phone'] = response.css('#contents > section > div > div:nth-child(1) > div.row > div.col-12.col-md-7.flex-grow-1 > div > table > tbody > tr:nth-child(2) > td > a::text').get('').strip()
        item['fax'] = response.css('#contents > section > div > div:nth-child(1) > div.row > div.col-12.col-md-7.flex-grow-1 > div > table > tbody > tr:nth-child(3) > td::text').get('').strip()
        item['email'] = response.css('#contents > section > div > div:nth-child(1) > div.row > div.col-12.col-md-7.flex-grow-1 > div > table > tbody > tr:nth-child(4) > td > a::text').get('').strip()
        item['homepage'] = response.css('#contents > section > div > div:nth-child(1) > div.row > div.col-12.col-md-7.flex-grow-1 > ul > li > a::attr(href)').get('').strip()
        introduce = response.css('#contents > section > div > div:nth-child(2) > div::text').extract()
        item['introduce'] = ''.join(introduce)
        
        yield item
        
        
        
        
