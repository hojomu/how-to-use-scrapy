import scrapy
import json
import os

from ..items import NaverMapItem

class NaverMapSpider(scrapy.Spider):
    name = "naverMap"
    allowed_domains = ["map.naver.com"]
    start_urls = ["https://map.naver.com"]
    
    subject = "2024_케이펫_수원2"
    
    custom_settings = {
        'FEEDS' : {
            f'results/{subject}/{subject}.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'store_empty': False,
                'fields': ['keyword', 'name','zip_code', 'address', 'phone', 'home_page', 'shortAddress', 'roadAddress', 'oldAddress'],
                'indent': 4,
            },
        },
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # 도메인 당 동시 요청 수 제한
        'CONCURRENT_REQUESTS_PER_IP': 1,  # IP 당 동시 요청 수 제한
        'ROBOTSTXT_OBEY' : False,
    }
    
    def __init__(self, *args, **kwargs):
        super(NaverMapSpider, self).__init__(*args, **kwargs)
        self.keywords1 = ["동탄", "위례", "고덕", "분당", "광교"]
        self.keywords2 = ["동물병원", "애견유치원", "애견카페"]
        self.keywords = self.generate_keywords()
        
        # self.keywords = [
            
        # ]
        
        self.current_index = 0  # 현재 키워드 인덱스
        self.current_page = 1   # 현재 페이지

    def generate_keywords(self):
        keywords = []
        for kw1 in self.keywords1:
            for kw2 in self.keywords2:
                keywords.append(f"{kw1} {kw2}")
        return keywords

    def start_requests(self):
        if self.keywords:
            yield self.make_request(self.keywords[self.current_index], self.current_page)

    def make_request(self, query, page):
        url = f"https://map.naver.com/p/api/search/allSearch?query={query}&type=all&searchCoord&boundary&page={page}"
        headers = {
            'authority': 'map.naver.com',
            'Accept': 'application/json, text/plain, */*',
            'Referer': f'https://map.naver.com/p/search/{query}?c=15.00,0,0,0,dh',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }
        return scrapy.Request(url, headers=headers, callback=self.parse, errback=self.errback, meta={'query': query, 'page': page})

    def parse(self, response):
        data = json.loads(response.text)
        results = data.get('result', {}).get('place', {}).get('list', []) # 해당 키가 없으면 오른쪽 파라미터를 리턴함. (error 발생 없이 넘어감)

        # 데이터를 수집하고 처리하는 코드
        for item in results:
            
            # address = ""
            # shortAddress = item.get('shortAddress', [])
            
            # if shortAddress is not None and len(shortAddress) > 0:
            #     address = " ".join(shortAddress)
            # else:
            #     address = item.get('roadAddress')
            yield {
                'keyword': self.keywords[self.current_index],
                'name': item.get('name'),
                'zip_code': '',
                'address': '',
                'phone': item.get('tel'),
                'home_page': item.get('homePage'),
                'shortAddress': item.get('shortAddress'),
                'roadAddress': item.get('roadAddress'),
                'oldAddress': item.get('address')
            }

        if results is None or len(results) < 20:
            self.current_index += 1
            self.current_page = 1
        else:
            self.current_page += 1

        if self.current_index < len(self.keywords):
            yield self.make_request(self.keywords[self.current_index], self.current_page)

    def errback(self, failure):
        self.current_index += 1
        self.current_page = 1
        if self.current_index < len(self.keywords):
            yield self.make_request(self.keywords[self.current_index], self.current_page)
