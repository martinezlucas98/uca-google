import unittest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import shutil
import os

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

if __name__ == '__main__':
    unittest.main()
