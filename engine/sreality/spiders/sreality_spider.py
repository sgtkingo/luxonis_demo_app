import time
import scrapy
import scrapy.exceptions
import scrapy_splash
from scrapy_splash import SplashRequest

script = """
function main(splash)
    splash:set_user_agent("facebot")
    assert(splash:go(splash.args.url))
    assert(splash:wait(0.5))

    local el = nil
    local max_cycles = 10 
    while max_cycles > 0 do
        if splash:select("div.property.ng-scope") then
            return splash:html()  -- Return HTML if the element is found
        else
            assert(splash:wait(0.5))
            max_cycles = max_cycles - 1
        end
    end
    return splash:html()
end
"""

# Splash settings
SPLASH_ARGS = {
    'wait': 0.1,  # Adjust based on page complexity   
    'lua_source': script,
    'render_all': 1,  # Load all resources (images, styles, scripts) 
    'http_method': 'GET',  # Use POST for submitting data, if needed,
}

class SrealitySpider(scrapy.Spider):
    name = "sreality"

    total = 50
    counter = 0
    progress = 0

    page_counter = 0
    baseurl = 'https://www.sreality.cz/hledani/prodej/byty?strana='

    def follow_url(self):
        self.page_counter += 1
        return f'{self.baseurl}{self.page_counter}'

    def start_requests(self):
        print("Waiting for Splash to load...")
        time.sleep(3)

        url = self.follow_url()
        yield SplashRequest(
            url, 
            endpoint='execute',
            callback=self.parse, 
            args=SPLASH_ARGS,
            slot_policy=scrapy_splash.SlotPolicy.SCRAPY_DEFAULT
            )

    def parse(self, response):
        #save response as HTML file
        #Path(f"sreality.html").write_bytes(response.body)
        #start parsing
        for property_item in response.css("div.property.ng-scope"):
                self.progress = int((self.counter/self.total)*100)
                print(f"Progress: {self.progress} %")

                self.counter+=1
                if self.counter <= self.total:
                    yield {
                        "title": property_item.css("span.name.ng-binding::text").get(),
                        "img": property_item.css("img").attrib.get('src')
                    } 
                else:
                    break           
        
        if self.counter <= self.total:
            next_page = self.follow_url()
            print('next page ->' + next_page)
            try:
                yield SplashRequest(
                    next_page, 
                    endpoint='execute',
                    callback=self.parse, 
                    args=SPLASH_ARGS,
                    slot_policy=scrapy_splash.SlotPolicy.SCRAPY_DEFAULT
                )
            except:
                raise scrapy.exceptions.CloseSpider('Next page doesnt exist')
