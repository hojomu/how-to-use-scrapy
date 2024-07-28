import scrapy
import json
import re
from scrapy.http import Request
from urllib.parse import urljoin, urlparse

class KaeaAdminSpider(scrapy.Spider):
    name = 'kaea_admin'
    
    custom_settings = {
        'ITEM_PIPELINES' : {
            'ScrapyFW.pipelines.KaeaPipeline': 300,
        },
        'FEEDS' : {
            'results/kaea/kaea DB.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'store_empty': False,
                'fields': ['name', 'zip_code', 'address', 'admin_office_num', 'homepage'],
                'indent': 4,
            },
        },
        'ROBOTSTXT_OBEY' : False
    }
    
    def start_requests(self):
        with open('results/kaea/highschool.json', 'r', encoding='utf-8') as file:
            self.schools = json.load(file)
        
        for school in self.schools:
            homepage = school.get('homepage')
            if homepage:
                yield Request(url=homepage, callback=self.parse_homepage, meta={'school': school})
                
    def parse_homepage(self, response):
        school = response.meta['school']
        content = response.text
        
        # 리다이렉션 확인 및 처리
        redirect_pattern = re.search(r'document.location.href\s*=\s*"(.*?)"', content)
        if redirect_pattern:
            redirect_url = redirect_pattern.group(1)
            full_redirect_url = urljoin(response.url, redirect_url)
            yield Request(url=full_redirect_url, callback=self.parse_redirected, meta={'school': school})
        else:
            yield from self.extract_admin_office(response, school)
    
    def parse_redirected(self, response):
        school = response.meta['school']
        yield from self.extract_admin_office(response, school)
    
    def extract_admin_office(self, response, school):
        content = response.text
        pattern = r'행정실\s*[:\s]*\(?(\d{2,3})\)?[) -]*(\d{3,4})[-\s]*(\d{4})'
        match = re.search(pattern, content)
        
        if match:
            admin_number = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
            school['admin_office_num'] = admin_number
        else:
            school['admin_office_num'] = None
        
        yield school