from pathlib import Path
import scrapy
import time
#from scrapy_splash import SplashRequest

class SrealitySpider(scrapy.Spider):
    name = "sreality"
    start_urls = [
        "https://www.sreality.cz/hledani/prodej/byty?strana=1"
    ]
    counter=500

    def start_requests(self):
        #yield SplashRequest(url=self.start_urls[0], callback=self.parse, args={'wait': 10})   
        yield scrapy.Request(url="https://www.sreality.cz/hledani/prodej/byty?strana=1", callback=self.parse) 

    def parse(self, response):
        for property_item in response.css("div.property.ng-scope"):
            print(self.counter)
            self.counter-=1
            if self.counter > 0:
                yield 
                {
                    "title": property_item.css("span.name.ng-binding::text").get(),
                    "img": property_item.css("img").attrib["src"].get()
                }
            else:
                return
        
        #next_page = response.css("li.paging-item a::attr(href)").get()
        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)
