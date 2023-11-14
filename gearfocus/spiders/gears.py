import scrapy
import json


class GearsSpider(scrapy.Spider):
    name = "gears"
    start_urls = ["http://gearfocus.com/"]

    def parse(self, response):
        pass
