import unittest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import shutil
import os
import json

if os.path.exists(os.getcwd() + '/spiders/uc_data/'):#comprueba si existe uc_data para eliminarlo
    shutil.rmtree(os.getcwd() + '/spiders/uc_data/')
else:
    print('no existe el directorio uc_data')
process = CrawlerProcess(get_project_settings())
process.crawl('testSpider')
process.start()

class spiderTest(unittest.TestCase):

    def test_data_exist(self):
        return self.assertTrue(os.path.exists(os.getcwd() + '/spiders/uc_data/'))

    def test_data_format(self):
        is_format_ok = False
        with open(os.getcwd() + '/spiders/uc_data/'+os.listdir(os.getcwd() + '/spiders/uc_data/')[0]) as f:
            data = json.load(f)
            is_format_ok = 'url_self' in data and 'url_html' in data and 'url_links' in data
            
        
        return self.assertTrue(is_format_ok)


if __name__ == '__main__':
    unittest.main()