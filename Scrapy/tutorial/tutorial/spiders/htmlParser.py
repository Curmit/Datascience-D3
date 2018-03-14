import scrapy

# 
# Run:
# scrapy crawl htmlparser
# 

class QuotesSpider(scrapy.Spider):
    name = "htmlparser"


    def start_requests(self):
        urls = [
            'https://www.monsterboard.nl/vacatures/zoeken/data-scientist_5?where=Groningen&cy=nl',
            'https://www.monsterboard.nl/vacatures/zoeken/data-scientist_5?where=Noord__2DHolland&cy=nl',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        endUrl = page.split("where=")
        function = endUrl[1]
        filename = 'quotes-%s.html' % function
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)