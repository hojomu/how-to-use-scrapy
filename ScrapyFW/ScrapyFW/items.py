# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyfwItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NHItem(scrapy.Item):
    name = scrapy.Field() # 농협 이름
    zip_code = scrapy.Field() # 우편번호
    address = scrapy.Field() # 주소
    phone = scrapy.Field() # 전화번호

class HighSchoolItem(scrapy.Item):
    name = scrapy.Field()
    zip_code = scrapy.Field()
    address = scrapy.Field()
    admin_office_num = scrapy.Field()
    homepage = scrapy.Field()

class InnovationMarketItem(scrapy.Item):
    keyword = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    item = scrapy.Field()
    businessNum = scrapy.Field()
    address = scrapy.Field()
    zipNo = scrapy.Field()
    tel = scrapy.Field()
    fax = scrapy.Field()
    homepage = scrapy.Field()
    category = scrapy.Field()
    manager = scrapy.Field()
    managerTel = scrapy.Field()
    managerEmail = scrapy.Field()
    
class NaverMapItem(scrapy.Item):
    keyword = scrapy.Field()
    name = scrapy.Field()
    zip_code = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    home_page = scrapy.Field()
    shortAddress = scrapy.Field()
    roadAddress = scrapy.Field()
    
class EurosatoryItem(scrapy.Item):
    name = scrapy.Field()
    country = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    hompage = scrapy.Field()
    
class InterbatteryItem(scrapy.Item):
    name = scrapy.Field()
    homepage = scrapy.Field()
    email = scrapy.Field()
    category = scrapy.Field()

class SidexItem(scrapy.Item):
    name = scrapy.Field()
    hall_number = scrapy.Field()
    booth_number = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    fax = scrapy.Field()
    email = scrapy.Field()
    homepage = scrapy.Field()
    introduce = scrapy.Field()

class ProconItem(scrapy.Item):
    name = scrapy.Field()
    email = scrapy.Field()
    homepage = scrapy.Field()
    products = scrapy.Field()

class RobotworldItem(scrapy.Item):
    name = scrapy.Field()
    email = scrapy.Field()
    homepage = scrapy.Field()
    category = scrapy.Field()
    category_detail = scrapy.Field()
    product_introduce = scrapy.Field()