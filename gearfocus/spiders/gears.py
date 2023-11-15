import scrapy
import json
from datetime import datetime

class GearsSpider(scrapy.Spider):
    name = "gears"
    categories =['digital-cameras-9', 'camera-lenses-filters-12', 'video-cameras-camcorders-27', 'lighting-studio-20', 'drones-aerial-imaging-10', 'computers-electronics-3', 'vintage-camera-equipment-40', 'video-production-editing-equipment-65', 'camera-accessories-76']

    def start_requests(self):
        url = "https://www.gearfocus.com/_next/data/QbGNbfaQztiSSCf1iieFJ/en/c/{}.json?page={}"
        for cat in self.categories:
            yield scrapy.Request(url.format(cat, 1), callback=self.parse_page1, meta={'category': cat, 'url': url})
    
    def parse_page1(self, response):
        #send current page to parse_page function
        yield self.parse_page(response)
        #Send the other pages to parse_page function
        url = response.meta['url']
        cat = response.meta['category']
        data = json.loads(response.text)
        total_pages = data['pageProps']['pageInfo']['totalPages']
        for page in range(2, total_pages+1):
            yield scrapy.Request(url.format(cat, page), callback=self.parse_page)
        
    def parse_page(self, response):
        data = json.loads(response.text)
        product_url = "https://www.gearfocus.com/products/{}"
        for item in data['pageProps']['results']:
            title = item['title']
            category = item['categories']
            original_price = item['og_price']
            current_price = item['price']
            stock = item['stock']
            if 'shipping_costs' in item:
                shipping_costs = item['shipping_costs'][0]['cost']
            else:
                shipping_costs = None
            listing_date = item['created'] / 1000
            listing_date = datetime.fromtimestamp(listing_date).date()
            condition = item['condition']
            brand = item['brand']
            description = item['description']
            item_url = product_url.format(item['slug'])
            o=dict()
            o['title'] = title
            o['category'] = category
            o['original_price'] = original_price
            o['current_price'] = current_price
            o['stock'] = stock
            o['shipping_costs'] = shipping_costs
            o['listing_date'] = listing_date
            o['condition'] = condition
            o['brand'] = brand
            o['description'] = description
            o['item_url'] = item_url
            yield o
            
            
            
            
