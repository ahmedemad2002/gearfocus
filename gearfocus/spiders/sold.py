import scrapy
import json


class SoldSpider(scrapy.Spider):
    name = "sold"
    
    def __init__(self, input_path=None):
        if input_path is None:
            input_path = 'data/curr_run.json'
        with open(input_path) as f:
            data = json.load(f)
        super(SoldSpider, self).__init__()
        self.URLs = [item['item_url'] for item in data]
    
    def start_requests(self):
        for url in self.URLs:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        res = response.css("#__NEXT_DATA__::text").get()
        res = json.loads(res)['props']['pageProps']
        yield {
            'URL': response.url,
            'Sold': res['product']['out_of_stock'],
        }
