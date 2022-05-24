# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class UrlInfo(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url_self = scrapy.Field()
    url_html = scrapy.Field()
    url_links = scrapy.Field()
