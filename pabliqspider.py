import scrapy


class PabliqspiderSpider(scrapy.Spider):
    name = "pabliqspider"
    allowed_domains = ["www.pabliq.se"]
    start_urls = ["http://www.pabliq.se/"]

    def parse(self, response):
        pass
