from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl('uc_spider')#, allowed_domains= allowed_domains, start_urls = start_urls)
process.start()