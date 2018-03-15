import scrapy
from scrapy.crawler import CrawlerProcess
import math as mt

opleiding = "Chemical Engineering"
globalTag = "Chemical Engineer wo"
outputdir = "CrawlerResults//test//testUrl.json"

class QuotesSpider(scrapy.Spider):
    name = "provincesMonsterboard"
    globalTag = ""


    def start_requests(self):
        provinces = ["Groningen",\
                    "Friesland",\
                    "Drenthe",\
                    "Overijssel",\
                    "Flevoland",\
                    "Gelderland",\
                    "Utrecht",\
                    "Noord__2DHolland",\
                    "Zuid__2DHolland",\
                    "Zeeland",\
                    "Noord__2DBrabant",\
                    "Limburg"]
        global globalTag
        # Start url
        
        # data-scientist_5?where=Noord__2DHolland&cy=nl'
        # Getting the tags from the input parameters
        tag = "boekhouder"
        # Globaltag is set to be able to add it to output file
        globalTag = tag
        # Tags are split i.e. "Data Scientist" gets split to build url
        tags = tag.split(" ")
        # "-" are added to indivitual tags for URL builder
        for i in range(len(tags)-1):
            tags[i] = tags[i] + "-"

        tags.append("_5?where=")
        # Correct url's are build format: "http://www.indeed.nl/data-scientist-vacatures-in-overijssel"
        # For each province there is a request done and the spider crawls the page
        for province in provinces:
            url = "https://www.monsterboard.nl/vacatures/zoeken/"
            for i in tags:
                url += str(i)
            url += province
            url += "&cy=nl"
            print(url)
            # response = scrapy.http.TextResponse(url=url)
            # header = response.xpath('//h2[contains(@class,"page-title visible-xs")]/text()').extract()
            # print(header)
            yield scrapy.Request(url=url, callback=self.parse)

    

    def parse(self, response):
    #     vacature = response.css('.result')[0]
    #     titles = vacature.xpath('//h2[contains(@class, "jobtitle")]/a/@title').extract()
        # locations = response.xpath('//div[contains(@class,"job-specs-location")]/p/a/text()').extract()
        # province = response.xpath('//input[contains(@placeholder,"Locatie")]/@value').extract()
        # titles = response.xpath('//div[contains(@class,"jobTitle")]/h2/a/text()').extract()  
        header = response.xpath('//h2[contains(@class,"page-title visible-xs")]/text()').extract()
        #companies = vacature.xpath('//div[contains(@data-tn-component, "organicJob")]/span[contains(@class, "company")]/text()').extract()
        headerList = [int(s) for s in header[0].split() if s.isdigit()]
        numberResult = headerList[0] if len(headerList) > 0 else 0 
        url = response.url
        urlList = []

        if numberResult > 25:
            pages = mt.ceil(numberResult/25)
            for i in range(1,pages + 1):
                urlList.append(url + "&page=" + str(i))

        
        #print("list size: " + str(len(titles)) + "locations size: " + str(len(locations)) + "companies size: " + str(len(companies)))
        for link in urlList:
            if numberResult > 0:
                yield {
                    'header': numberResult,
                    'url': link,
                }
        
            
        # next_page = response.xpath('//span[@class="np" and contains(.,"Volgende")]/../../@href').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'FEED_URI': outputdir
})

process.crawl(QuotesSpider)
process.start() # the script will block here until the crawling is finished