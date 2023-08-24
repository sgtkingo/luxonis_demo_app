from pathlib import Path
import scrapy
from scrapy_splash import SplashRequest

"""
class TestSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):
``      urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
"""

"""
class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]
    max_pages = 5

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None and self.max_pages > 0:
            print(f'-> next page found! {self.max_pages}/5')
            self.max_pages -= 1
            yield response.follow(next_page, callback=self.parse)    
"""
lua_script = """
function main(splash, args)
    assert(splash:go(args.url))

    while not splash:select('div.quote') do
        splash:wait(0.5)
        print('waiting...')
    end
    return {html=splash:html()}
end
""" 

class TestSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):
        # url = 'https://quotes.toscrape.com/js/'
        # yield SplashRequest(url, callback=self.parse, args={'wait': 0.5})
        url = 'https://quotes.toscrape.com/scroll'
        yield SplashRequest(
            url, 
            callback=self.parse, 
            endpoint='execute', 
            args={'wait': 0.5, 'lua_source': lua_script}
            )        

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }      
