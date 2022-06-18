# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Dict
from attr import asdict, has
from itemadapter import ItemAdapter
import hashlib
import json
import os
import errno

class CrawlerPipeline:
    def process_item(self, item, spider):
        
        url = item['url_self'][0].encode('utf-8')

        hash = hashlib.md5(url).hexdigest()
        
        try:
            os.mkdir(os.getcwd() + '/spiders/uc_data')
        except OSError as e:
            if e.errno != errno.EEXIST:
                pass
    
        file = open(os.getcwd() + '/spiders/uc_data/uc_' + hash + '.json', "w+")
        json.dump(dict(item), file, indent = 4)
        file.close

