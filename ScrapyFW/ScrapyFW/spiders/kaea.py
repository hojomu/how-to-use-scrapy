import scrapy
from ..items import HighSchoolItem

class KaeaSpider(scrapy.Spider):
    name = 'kaea'
    allowed_domains = ['ffk.or.kr']
    start_urls = ['https://ffk.or.kr/subList/10000004221']
    
        # 'ITEM_PIPELINES' : {
        #     'ScrapyFW.pipelines.KaeaPipeline': 300,
        # },
        
    custom_settings = {
        'FEEDS' : {
            'results/kaea/highschool.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'store_empty': False,
                'fields': ['name', 'zip_code', 'address', 'admin_office_num', 'homepage'],
                'indent': 4,
            },
        }
    }
    
    def parse(self, response):
        schools = response.css('#cntntsCn > table.table00.num.__se_tbl > tbody > .tbody')
        for school in schools:
            tds = school.css('td')
            flag_num = 1 if len(tds) > 4 else 0
            
            yield HighSchoolItem(
                name = tds[flag_num].css('::text').get().strip('★ '),
                zip_code = tds[2+flag_num].css('::text').get().strip(),
                address = tds[3+flag_num].css('::text').get().strip(),
                homepage = tds[3+flag_num].css('::attr(href)').get().strip(),
            )