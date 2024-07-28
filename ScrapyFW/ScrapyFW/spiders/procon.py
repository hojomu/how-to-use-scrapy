import scrapy
import os
from ..items import ProconItem


class ProconSpider(scrapy.Spider):
    name = "procon"
    allowed_domains = ["www.procon.co.kr"]
    start_urls = ["https://www.procon.co.kr"]
    
    subject = 'procon'
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapyFW.pipelines.BasicJsonPipeline': 300
        },
        'ROBOTSTXT_OBEY' : False,
    }
    
    def __init__(self, *args, **kwargs):
        super(ProconSpider, self).__init__(*args, **kwargs)
        self.page = 1
        self.crawl_state = True
        self.basic_url = 'http://www.procon.co.kr/bbs/board.php?bo_table=company_info&page='

        self.pipeline_output_path = os.path.join('results',f'{self.subject}',f'{self.subject}.json')
        if not os.path.exists(os.path.dirname(self.pipeline_output_path)):
            os.makedirs(os.path.dirname(self.pipeline_output_path))
            
        self.detail_num = 0
        
    def start_requests(self):
        url = f"{self.basic_url}{self.page}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        tbody = response.css('#fboardlist > div > table > tbody')
        links = tbody.css('a::attr(href)').extract()
        
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_detail)
        
        amount_of_links = len(links)
        
        if amount_of_links < 10:
            self.crawl_state = False
        elif amount_of_links == 15:
            self.page += 1
        
        if self.crawl_state:
            url = f"{self.basic_url}{self.page}"
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse_detail(self, response):
        self.detail_num += 1
        print(f"detail number = {self.detail_num}")
        
        tbody = response.css('#bo_v_con tbody')

        item = ProconItem()
        item['name'] = tbody.css('tr:nth-child(1) > td::text').get('').strip()
        item['email'] = tbody.css('tr:nth-child(5) > td::text').get('').strip()
        item['homepage'] = tbody.css('tr:nth-child(6) a::text').get('').strip()
        item['products'] = tbody.css('tr:nth-child(7) > td::text').get('').strip()
        
        yield item