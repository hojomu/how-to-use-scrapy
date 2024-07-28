import scrapy
import re
import urllib.parse
from scrapy.http import FormRequest
from ..items import InnovationMarketItem

class InnovationmarketSpider(scrapy.Spider):
    name = "innovationMarket"
    allowed_domains = ["ppi.g2b.go.kr"]
    start_urls = ["https://ppi.g2b.go.kr:8914"]
    
    custom_settings = {
        'FEEDS' : {
            'results/innovationMarket/innovationMarket_url_7.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'store_empty': False,
                'fields': ['category','name', 'url'],
                'indent': 4,
            },
        }
    }

    def parse(self, response):
        # 초기 요청을 위한 URL
        url = "https://ppi.g2b.go.kr:8914/sm/dm/sch/searchGoodsList.do"
        headers = {
            'Cookie': 'JSESSIONID=fPz3mMtF2yTFt7LHCccTTTPsnY1LDttT1nhdrGl2Q9B3Cqvm8CtS!1794135408; WMONID=5VJX-q_gE18'
        }
        
        lrgeCtgrNm = urllib.parse.quote('디지털/가전', safe='/')
        middlCtgrNm = urllib.parse.quote('기타 전자제품', safe='/')
        smallCtgrNm = urllib.parse.quote('기타 전자', safe='/')

        # 순차적으로 'from' 값을 변경하여 요청
        for i in range(1, 5):  # 'from' 값을 a에서 (b-1)까지 1씩 증가시킴
            payload = {
                'invGdsIdntNo': '',
                'srchwrd': '',
                'keyword': '',
                'viewType': '',
                'corpNm': '',
                'prdctClsfcNm': '',
                'invCertiNms': '',
                'corpCertiNms': '',
                'prdctCertiNms': '',
                'invCertPblctnSbjctNms': '',
                'lrgeCtgrNm': lrgeCtgrNm,
                'middlCtgrNm': middlCtgrNm,
                'smallCtgrNm': smallCtgrNm,
                'subCategory': 'mall',
                'attrNm': '',
                'attrMergeInfo': '',
                'sorts': '_score^desc',
                'isRprsntGds': 'Y',
                'regions': '',
                'size': '10',
                'from': str(i),
                'sort': '_score%5Edesc',
                'pageUnit': '10',
                'lrgeCtgrNo': '',
                'middlCtgrNo': '',
                'smallCtgrNo': '',
                'startPrice': '',
                'endPrice': ''
            }

            yield FormRequest(
                url,
                formdata=payload,
                headers=headers,
                callback=self.parse_results,
                dont_filter=True  # 중복 필터링을 비활성화하여 동일한 URL에 대한 요청을 허용합니다.
            )

    def parse_results(self, response):
        lis = response.css('#listView > ul > li')
        for li in lis:
            href = li.css('.item_img_box > a::attr(href)').get().strip()
            match = re.search(r"fnDetail\('(\d+)'\)", href)
            
            domain = 'https://ppi.g2b.go.kr:8914/sm/dm/sch/searchGoodsDetail.do?invGdsIdntNo='
            yield InnovationMarketItem(
                category = '기타 전자',
                name = li.css('.item_list_info > .item_end_area > dl > dd > span::text').get().strip(),
                url = domain + match.group(1),
            )