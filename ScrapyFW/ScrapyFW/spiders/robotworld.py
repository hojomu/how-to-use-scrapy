import scrapy
import os
from ..items import RobotworldItem


class RobotworldSpider(scrapy.Spider):
    name = "robotworld"
    allowed_domains = ["www.robotworld.or.kr"]
    start_urls = ["https://www.robotworld.or.kr"]
    
    subject = 'robotworld'
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapyFW.pipelines.BasicJsonPipeline': 300
        },
        'ROBOTSTXT_OBEY' : False,
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',  # 중복 필터 비활성화
    }
    
    def __init__(self, *args, **kwargs):
        super(RobotworldSpider, self).__init__(*args,**kwargs)
        self.page = 1
        self.crawl_state = True
        self.basic_url = 'https://www.robotworld.or.kr/visitors/list_of_exhibitors.php?offset='
        
        self.pipeline_output_path = os.path.join('results', f'{self.subject}', f'{self.subject}.json')
        if not os.path.exists(os.path.dirname(self.pipeline_output_path)):
            os.makedirs(os.path.dirname(self.pipeline_output_path))
        
        self.detail_num = 0
        
    def start_requests(self):
        offset = 10 * (self.page - 1)
        url = f"{self.basic_url}{offset}"
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        table = response.css('table')
        trs = table.css('tbody > tr')
        
        amount_of_trs = len(trs)
        
        for tr in trs:
            data = {
                'href': tr.css('td:nth-child(3) > a::attr(href)').get(''),
                'name': tr.css('td:nth-child(3) > a::text').get('').strip(),
                'homepage': tr.css('td:nth-child(7) > a::text').get('').strip(),
                'category': tr.css('td:nth-child(5)::text').get('').strip(),
                'category_detail': tr.css('td:nth-child(6)::text').get('').strip()
            }
            link = f'{self.start_urls[0]}{data['href']}'
            
            yield scrapy.Request(url=link, callback=self.parse_detail , meta=data)
            
        if amount_of_trs < 10:
            self.crawl_state = False
        elif amount_of_trs == 10:
            self.page += 1
        
        if self.crawl_state:
            offset = 10 * (self.page - 1)
            url = f"{self.basic_url}{offset}"
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse_detail(self, response):
        meta_data = response.meta
        
        data = {
            'name': response.css('tbody > tr:nth-child(1) > td::text').get('').strip(),
            'homepage': response.css('tbody > tr:nth-child(8) > td > a::text').get('').strip(),
            'email': response.css('tbody > tr:nth-child(7) > td::text').get('').strip(),
            'product_introduce': "\n".join(response.css('tbody > tr:nth-child(11) > td::text').getall())
        }
        
        item = RobotworldItem()
        
        item['name'] = data['name'] if data['name'] else meta_data['name']
        item['email'] = data['email']
        item['homepage'] = data['homepage'] if data['homepage'] else meta_data['homepage']
        item['category'] = meta_data['category']
        item['category_detail'] = meta_data['category_detail']
        item['product_introduce'] = data['product_introduce']
        
        yield item
