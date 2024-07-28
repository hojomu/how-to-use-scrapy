import scrapy
import json
from scrapy.http import Request
from ..items import InnovationMarketItem



class InnovationmarketDetailSpider(scrapy.Spider):
    name = "innovationMarket_detail"
    
    custom_settings = {
        'FEEDS' : {
            'results/innovationMarket/innovationMarket.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'store_empty': False,
                'fields': ['keyword', 'name', 'url', 'item', 'businessNum',
                           'address', 'zipNo', 'tel', 'fax', 'homepage',
                           'category', 'manager', 'managerTel', 'managerEmail'],
                'indent': 4,
            },
        }
    }
    
    def start_requests(self):
        for i in range(1,8):
            if i == 3:
                continue
            with open(f'results/innovationMarket/innovationMarket_url_{i}.json', 'r', encoding='utf-8') as file:
                if i == 1:
                    self.innovationMarkets = json.load(file)
                else:
                    self.innovationMarkets.extend(json.load(file))
                
        print(f'{len(self.innovationMarkets)} 개의 데이터를 수집합니다.')
            
        for innovationMarket in self.innovationMarkets:
            url = innovationMarket.get('url')
            if url:
                yield Request(url=url, callback=self.parse_homepage, meta={'innovationMarket': innovationMarket})
            
    def parse_homepage(self, response):
        innovationMarket = response.meta['innovationMarket']
        
        yield InnovationMarketItem(
            keyword = innovationMarket.get('category'),
            name = innovationMarket.get('name'),
            item = response.css('#main01 > div.sm_cont > section > div > div.item_info_box > div.item_topinfo_head > div.item_case_basic > h2::text').get().strip(),
            businessNum = response.css('#bizrInfoBox > div:nth-child(2) > div > dl:nth-child(1) > dd:nth-child(2)::text').get().strip(),
            address = response.css('#bizrInfoBox > div:nth-child(2) > div > dl:nth-child(1) > dd:nth-child(4)::text').get().strip(),
            zipNo = response.css('#bizrInfoBox > div:nth-child(2) > div > dl:nth-child(2) > dd:nth-child(4)::text').get().strip(),
            tel = response.css('#bizrInfoBox > div:nth-child(2) > div > dl:nth-child(1) > dd:nth-child(6)::text').get().strip(),
            fax = response.css('#bizrInfoBox > div:nth-child(2) > div > dl:nth-child(2) > dd:nth-child(6)::text').get().strip(),
            homepage = response.css('#bizrInfoBox > div:nth-child(2) > div > dl:nth-child(1) > dd:nth-child(8)::text').get().strip(),
            category = response.css('#bizrInfoBox > div:nth-child(2) > div > dl:nth-child(2) > dd:nth-child(8)::text').get().strip(),
            manager = response.css('#ofclNm::text').get().strip(),
            managerTel = response.css('#ofclTelNo::text').get().strip(),
            managerEmail = response.css('#ofclEmail::text').get().strip()
        )