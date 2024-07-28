import scrapy
import json
from ..items import InterbatteryItem

class InterbatterySpider(scrapy.Spider):
    name = "interbattery"
    allowed_domains = ["interbattery.or.kr"]
    start_urls = ["https://interbattery.or.kr"]
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapyFW.pipelines.InterbatteryPipeline': 300
        },
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # 도메인 당 동시 요청 수 제한
        'CONCURRENT_REQUESTS_PER_IP': 1,  # IP 당 동시 요청 수 제한
        'ROBOTSTXT_OBEY' : False,
    }
    
    def __init__(self, *args, **kwargs):
        super(InterbatterySpider, self).__init__(*args, **kwargs)
        self.selPageNo = 1
        self.crawl_state = True

    def start_requests(self):
        url = "https://interbattery.or.kr/fairOnline.do"
        headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json;charset=UTF-8',
                'Cookie': 'JSESSIONID=ACB7A8D1D4087DBABAE58E4DE27C59B3; _ga=GA1.1.58451493.1719274145; _ga_CRYFR3H66C=GS1.1.1719274145.1.1.1719274367.0.0.0',
                'Host': 'interbattery.or.kr',
                'Origin': 'https://interbattery.or.k',
                'Pragma': 'no-cache',
                'Referer': 'https://interbattery.or.kr/fairOnline.do?selAction=single_page&SYSTEM_IDX=122&FAIRMENU_IDX=17933&hl=KOR',
                'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
                }
        
        payload = {
            "SYSTEM_IDX": 122,
            "archive": "2024",
            "EX_FORM_ID": "interbattery_FAIR_01",
            "order_first_input_id": "mod5553_in1",
            "order_first_input_val": "in3",
            "order_custom_input_id": "mod5553_in4",
            "selPageNo": str(self.selPageNo)}
        
        yield scrapy.Request(url=url, method="POST", headers=headers, body=json.dumps(payload), callback=self.parse)

    def parse(self, response):
        try:
            data_json = response.json()
        except json.JSONDecodeError:
            self.logger.error(f"Failed to decode JSON: {response.text}")
            return

        datas = data_json.get('prodList', [])
        amount = len(datas)
        
        if amount < 10:
            self.crawl_state = False
        elif amount == 10:
            self.selPageNo += 1

        for data in datas:
            categorys = data.get('item_category_json', [])
            corp_category = ''.join([category.get('n', '') for category in categorys])

            item = InterbatteryItem()
            item['name'] = data.get('corp_nm_kor', '')
            item['homepage'] = data.get('corp_homepage', '')
            item['email'] = data.get('corp_email', '')
            item['category'] = corp_category

            yield item
        
        if self.crawl_state:
            self.logger.info(f"Fetching next page: {self.selPageNo}")
            url = "https://interbattery.or.kr/fairOnline.do"
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json;charset=UTF-8',
                'Host': 'interbattery.or.kr',
                'Origin': 'https://interbattery.or.kr',
                'Pragma': 'no-cache',
                'Referer': 'https://interbattery.or.kr/fairOnline.do?selAction=single_page&SYSTEM_IDX=122&FAIRMENU_IDX=17933&hl=KOR',
                'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
            }
            
            payload = {
                "SYSTEM_IDX": 122,
                "archive": "2024",
                "EX_FORM_ID": "interbattery_FAIR_01",
                "order_first_input_id": "mod5553_in1",
                "order_first_input_val": "in3",
                "order_custom_input_id": "mod5553_in4",
                "selPageNo": self.selPageNo
            }
            
            yield scrapy.Request(url, method="POST", headers=headers, body=json.dumps(payload), callback=self.parse)
