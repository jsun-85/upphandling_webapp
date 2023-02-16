import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from myproject.items import MyItem


class MySpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ['www.pabliq.se']
    start_urls = ['https://www.pabliq.se/sokresultat?q=vibration']

    def parse(self, response):
        rows = response.xpath("//table[@class='table table-striped']/tbody/tr")
        for row in rows:
            loader = ItemLoader(item=MyItem(), selector=row)
            loader.add_xpath('col1', './td[1]/text()')
            loader.add_xpath('col2', './td[2]/text()')
            loader.add_xpath('col3', './td[3]/text()')
            loader.add_xpath('col4', './td[4]/text()')
            loader.add_xpath('link', './td[5]//a/@href')
            yield loader.load_item()