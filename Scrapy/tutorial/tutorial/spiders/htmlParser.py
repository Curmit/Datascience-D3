import scrapy
import json

# 
# Run:
# scrapy crawl htmlparser
# 

class QuotesSpider(scrapy.Spider):
    name = "htmlparser"


    def start_requests(self):
        urls = json.load(open('../../CrawlerResults/test/testUrl.json'))
        for url in urls:
            yield scrapy.Request(url=url['url'], callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        endUrl = page.split("page=")
        function = endUrl[1]
        filename = 'quotes-%s.html' % function
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)