# Script to generate the URL's from Monsterboard ready for crawling

```

import scrapy
from scrapy.crawler import CrawlerProcess
import math as mt

# Script generates a JSON file of format 'jobname'.json containing all the URLs of Monsterboard split up over different pages
# i.e. when searching for a certain vacancy Monsterboard responds with a result possibly split up over multiple pages
# for each page there is a URL created. For example if Monsterboard responds with 10 pages of results the output JSON file
# will contain 10 URLs which are suitable for scraping on a deeper level (and used in monsterboardScrapingScript.py).

globalTag = "Process technology wo"
outputdir = "CrawlerResults//urls//" + globalTag +".json"

class QuotesSpider(scrapy.Spider):
    name = "provincesMonsterboard"

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
        # Variable set for the job name
        global globalTag

        # Tags are split i.e. "Data Scientist" gets split to build url
        tags = globalTag.split(" ")
        # "-" are added to indivitual tags for URL builder
        for i in range(len(tags)-1):
            tags[i] = tags[i] + "-"

        # String added for the complete monsterboard URL
        tags.append("_5?where=")

        # Correct url's are build format for monsterboard vacancy Accountant, province = Utrecht: ""https://www.monsterboard.nl/vacatures/zoeken/Accountant-wo_5?where=Utrecht&cy=nl&page=2""
        
        # For each province there is a request done (url generated) and the spider crawls the page
        for province in provinces:
            url = "https://www.monsterboard.nl/vacatures/zoeken/"
            for i in tags:
                url += str(i)
            url += province
            url += "&cy=nl"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
  
        # Xpath location of the province value on the page (outcome = one of the province)
        province = response.xpath('//input[contains(@placeholder,"Locatie")]/@value').extract()[0]
        # Xpath location of header of Monsterboard which contains a number representing the number of vacancies (searchresults)
        header = response.xpath('//h2[contains(@class,"page-title visible-xs")]/text()').extract()
        if len(header) == 0:
            header.append("empty")
        headerList = [int(s) for s in header[0].split() if s.isdigit()]
        # Header is used to extract the number of searchresults from Monsterboard
        numberResult = headerList[0] if len(headerList) > 0 else 0 
        url = response.url
        urlList = []
        
        # Each page represents 25 results. Total amount of resuls are divided by 25 to create the correct amount of pages
        pages = mt.ceil(numberResult/25)
        for i in range(1,pages + 1):
            urlList.append(url + "&page=" + str(i))


        # loop which creates the JSON format as output file containing, reportedResults, URL, PageNumber, Province
        for i in range(0,len(urlList)):
            if numberResult > 0:
                yield {
                    'reportedResults': numberResult,
                    'url': urlList[i],
                    'pageNumber': i + 1,
                    'province': province,
                }
        
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'DOWNLOAD_DELAY': 2,
    'FEED_URI': outputdir,
    'COOKIES_ENABLED': False,
})

process.crawl(QuotesSpider)
process.start() # the script will block here until the crawling is finished

```