# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
import pandas as pd
import os


class ScrapyfwPipeline:
    def process_item(self, item, spider):
        return item

class NHPipeline:
    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        for field in adapter:
            if isinstance(adapter[field], str):
                if field == 'zip_code':
                    adapter[field] = adapter[field].strip('()')
                    
                adapter[field] = adapter[field].strip()
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        with open('results/nh/results.json', 'w') as file:
            json.dump(self.items, file)

        df = pd.read_json('results/nh/results.json')
        df.to_excel('results/nh/results.xlsx', index=False)
    
class KaeaPipeline:
    def open_spider(self,spider):
        self.schools = []
    
    def process_item(self, item, spider):
        self.schools.append(item)
        return item
    
    def close_spider(self, spider):
        df = pd.DataFrame(self.schools)
        df.to_excel('results/kaea/kaea DB.xlsx', index=False)
    
class EurosatoryPipeline:
    def open_spider(self, spider):
        file_path = os.path.join('results', 'eurosatory', 'eurosatory.json')
        self.file = open(file_path, 'w', encoding='utf-8')
        self.file.write("[\n")
        
    def close_spider(self, spider):
        self.file.seek(self.file.tell() - 2, os.SEEK_SET)
        self.file.write("\n]")
        self.file.close()
        
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + ",\n"
        self.file.write(line)
        
        return item
    
class InterbatteryPipeline:
    def open_spider(self, spider):
        file_path = os.path.join('results','interbattery','interbattery.json')
        self.file = open(file_path, 'w', encoding='utf-8')
        self.file.write("[\n")

    def close_spider(self,spider):
        self.file.seek(self.file.tell() - 2, os.SEEK_SET)
        self.file.write("\n]")
        self.file.close()
        
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + ",\n"
        self.file.write(line)
        
        return item

class BasicJsonPipeline:
    def open_spider(self, spider):
        file_path = spider.pipeline_output_path
        self.file = open(file_path, 'w', encoding='utf-8')
        self.file.write("[\n")

    def close_spider(self,spider):
        self.file.seek(self.file.tell() - 2, os.SEEK_SET)
        self.file.write("\n]")
        self.file.close()
        
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + ",\n"
        self.file.write(line)
        
        return item
