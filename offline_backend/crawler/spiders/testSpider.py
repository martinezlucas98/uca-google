import hashlib
from multiprocessing import process
from urllib import response
import scrapy
import sys
import os
from scrapy.spiders import CrawlSpider, Rule
from crawler.items import UrlInfo
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
# from spiders import uc_spider


class testSpider(CrawlSpider):
    name = 'testSpider'
    allowed_domains = ['www.universidadcatolica.edu.py']
    start_urls = ['http://www.universidadcatolica.edu.py']
    handle_httpstatus_list = [500]
    extractor = LinkExtractor(allow_domains='www.universidadcatolica.edu.py', allow='/identidad')
    rules = (
        Rule(link_extractor=extractor, callback='parse_item',
             errback='error_handler', follow=True),
        # se define al metodo "parse_item" como callback del link extractor
    )

    def parse_item(self, response):
        # se inicializa el cargador de items
        loader = ItemLoader(item=UrlInfo(), response=response)
        # se cargan los campos del item "UrlInfo" con la informacion obtenida de cada url
        loader.add_value('url_self', response.url)
        loader.add_value('url_html', response.text)
        loader.add_value('url_links',
                         self.list_to_dict(url_list=self.extractor.extract_links(response)))
        # se retorna el item cargado de datos para procesar en pipelines.py
        return loader.load_item()

    def error_handler(self, failure):
        self.log('Error de tipo ' + str(failure.value))

    # se retorna una lista de diccionarios cuyo contenido es el enlace "url"
    def list_to_dict(self, url_list):
        # la direccion de un archivo json que corresponde a los datos de esa url "path"
        url_list_dict = []
        for link in url_list:
            link_string = link.url
            url_hash = hashlib.md5(str(link_string).encode(
                'utf-8'))  # se obtiene el hash de la url
            url_dict = {
                "url": str(link_string),
                "path": os.getcwd() + '/spiders/uc_data/uc_' + url_hash.hexdigest() + '.json'
            }  # nombre del archivo = uc_[hash de su url].json
            url_list_dict.append(url_dict)

        return url_list_dict
