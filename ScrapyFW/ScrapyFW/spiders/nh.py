import scrapy
from ..items import NHItem

class NhSpider(scrapy.Spider):
    name = "nh"
    allowed_domains = ["www.nonghyup.com"]
    start_urls = ["https://www.nonghyup.com/introduce/organization/nhInfo.do"]
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'ScrapyFW.pipelines.NHPipeline': 300,
        }
    }
    
    def __init__(self, *args, **kwargs):
        super(NhSpider,self).__init__(*args,**kwargs)
        self.page_index = 1
        
    def start_requests(self):
        yield from self.request_page(self.page_index)

    def parse(self, response):
        rows = response.css('#contents > div.mt10 > div.tb > table > tbody > tr')
        for row in rows:
            yield NHItem(
                name = row.css('td:nth-child(1)::text').get(),
                zip_code = row.css('td:nth-child(2)::text').get(),
                address = row.css('td:nth-child(3)::text').get(),
                phone = row.css('td:nth-child(4)::text').get(),
            )
        
        if len(rows) == 20:
            self.page_index += 1
            yield from self.request_page(self.page_index)
            
    def request_page(self, page_index):
        url = self.start_urls[0]
        headers = {
            'Cookie': 'PSNP_SSID=eLYw7sTJfZULIIkFx8zpgX75mBaQaEB2FSTGYHaPqOSlVs3Lzrvh5MRjo9YD5P9l.UFNOUC9uaGVybmhsb3dzMDFfcHNucDAx'
        }
        payload = {
            'pageIndex': str(page_index),
            'indexRegion': 'entire',
            'searchCcwnm': '',
            'searchWrd': ''
        }
        
        yield scrapy.FormRequest(url, formdata=payload, headers=headers, callback=self.parse)