import unittest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
#ejecuta uc_spider
#process.crawl('uc_spider')
#process.start()

class uc_spider_test(unittest.TestCase):

    pass