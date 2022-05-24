import hashlib
import scrapy
import os
from scrapy.spiders import CrawlSpider, Rule
from crawler.items import UrlInfo
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor

class UcSpiderSpider(CrawlSpider):
    name = 'uc_spider'
    allowed_domains = ['universidadcatolica.edu.py']
    start_urls = ['https://www.universidadcatolica.edu.py/']
    extractor = LinkExtractor(allow_domains = 'universidadcatolica.edu.py')
    rules = (
        Rule(link_extractor = extractor , callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        loader = ItemLoader(item=UrlInfo(), response=response)
        loader.add_value('url_self', response.url)
        loader.add_value('url_html', response.text)
        loader.add_value('url_links', 
        self.list_to_dict(url_list = self.extractor.extract_links(response) ) 
            )
        return loader.load_item()

    def list_to_dict(self, url_list):
        url_list_dict = []
        for link in url_list:
            link_string = link.url
            url_hash = hashlib.md5(str(link_string).encode('utf-8'))
            url_dict = {
                "url": str(link_string),
                "path": os.getcwd() + '/crawler/spiders/uc_data/uc_' + url_hash.hexdigest() + '.json'
            }
            url_list_dict.append(url_dict)

        return url_list_dict
