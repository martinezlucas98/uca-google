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
        #se define al metodo "parse_item" como callback del link extractor
    )

    def parse_item(self, response):
        loader = ItemLoader(item=UrlInfo(), response=response) #se inicializa el cargador de items
        # se cargan los campos del item "UrlInfo" con la informacion obtenida de cada url
        loader.add_value('url_self', response.url)
        loader.add_value('url_html', response.text)
        loader.add_value('url_links', 
        self.list_to_dict(url_list = self.extractor.extract_links(response) ) 
            )
        return loader.load_item() # se retorna el item cargado de datos para procesar en pipelines.py

    def list_to_dict(self, url_list): # se retorna una lista de diccionarios cuyo contenido es el enlace "url"
        url_list_dict = []            # la direccion de un archivo json que corresponde a los datos de esa url "path"
        for link in url_list:
            link_string = link.url
            url_hash = hashlib.md5(str(link_string).encode('utf-8')) #se obtiene el hash de la url 
            url_dict = {
                "url": str(link_string),
                "path": os.getcwd() + '/spiders/uc_data/uc_' + url_hash.hexdigest() + '.json' 
            }       #nombre del archivo = uc_[hash de su url].json
            url_list_dict.append(url_dict)

        return url_list_dict
