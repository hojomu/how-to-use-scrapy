import scrapy
import json
import os
from ..items import EurosatoryItem

class EurosatorySpider(scrapy.Spider):
    name = "eurosatory"
    allowed_domains = ["www.eurosatory.com"]
    start_urls = ["https://www.eurosatory.com"]
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapyFW.pipelines.EurosatoryPipeline': 300
        },
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # 도메인 당 동시 요청 수 제한
        'CONCURRENT_REQUESTS_PER_IP': 1,  # IP 당 동시 요청 수 제한
        'ROBOTSTXT_OBEY' : False,
    }
    
    def __init__(self, *args, **kwargs):
        super(EurosatorySpider, self).__init__(*args, **kwargs)
        file_path = os.path.join('results', 'eurosatory', 'all_ids.json')
        with open(file_path,'r',encoding='utf-8') as file:
            self.ids = json.load(file)
            
    def start_requests(self):
        ids = self.ids
        basic_url = 'https://eurosatory.finderr.cloud/api/catalog/get_exhibitor/'
        for id in ids:
            url = basic_url + str(id) + '/en'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = response.json()
        
        item = EurosatoryItem()
        item['name'] = data.get('Exhi_CompanyName')
        item['country'] = data.get('Exhi_Country_Name')
        item['email'] = data.get('Exhi_ContactEmail')
        item['phone'] = data.get('Exhi_Phone')
        item['hompage'] = data.get('Exhi_Website')
        
        yield item
        
