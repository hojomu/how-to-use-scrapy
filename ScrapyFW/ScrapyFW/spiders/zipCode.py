import scrapy
import json
import os
from ..items import NaverMapItem


class ZipcodeSpider(scrapy.Spider):
    name = "zipCode"
    allowed_domains = ["business.juso.go.kr"]
    start_urls = ["https://business.juso.go.kr/addrlink/addrLinkApi.do"]

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter', # 중복 필터링 비활성화
        'FEEDS' : {
            'results/2024cafSeoulItem/2024cafSeoulItem_zipNo.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'store_empty': False,
                'fields': ['keyword', 'name','zip_code', 'address', 'phone', 'home_page', 'shortAddress', 'roadAddress', 'oldAddress'],
                'indent': 4,
            },
        }
    }
    
    def __init__(self, *args, **kwargs):
        super(ZipcodeSpider,self).__init__(*args,**kwargs)
        
        self.json_file_path = r'results/2024cafSeoulItem/2024cafSeoulItem_unique.json'
        # 개발용 키 : ~ 2024/09/19
        self.api_key = 'devU01TX0FVVEgyMDI0MDYyMTExMjMxNTExNDg1ODk='
    
    def start_requests(self):
        json_file_path = r'results/2024cafSeoulItem/2024cafSeoulItem_unique.json'
        
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    
        for data in json_data:
            keyword = ""
            shortAddress = data.get('shortAddress', [])
            roadAddress = data.get('roadAddress', '')
            oldAddress  = data.get('oldAddress', '')
            
            if shortAddress and len(shortAddress) > 1:
                keyword = f"{shortAddress[0]} {shortAddress[1]}"
            elif roadAddress:
                keyword = roadAddress
            elif oldAddress:
                keyword = oldAddress
                
            if keyword:
                url = f"https://business.juso.go.kr/addrlink/addrLinkApi.do?confmKey={self.api_key}&currentPage=1&countPerPage=10&keyword={keyword}&resultType=json"
                headers = {
                    'Cookie': 'clientid=020088030481; elevisor_for_j2ee_uid=6rz56xwzqfmkj'
                }
                yield scrapy.Request(url, callback=self.parse, headers=headers, meta={'data':data})
    
    def parse(self, response):
        data = response.meta['data']
        
        # json_response = json.loads(response.text)
        json_data = response.json()
        
        if 'results' in json_data and 'juso' in json_data['results'] and len(json_data['results']['juso']) > 0:
            zip_code = json_data['results']['juso'][0].get('zipNo', '')
        else:
            zip_code = ''
            
        data['zip_code'] = zip_code
        
        yield data
        
        
        # 테스트 실행 코드
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(ZipcodeSpider)
    process.start()