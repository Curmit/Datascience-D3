import scrapy
from scrapy.crawler import CrawlerProcess
import math as mt
import json

# CREATED BY:
# Carmen Burghardt (Master student Creative Technology @ University of Twente)
# Rick Lenderink (Master student Business Information Technology @ University of Twente)
# 
# 
# Scraping script designed for http://wwww.monsterboard.nl/ in order to get, given a certain jobsearch + province, 
# the job title and job location. 
# 
# This information is used to give a visual representation of the amount of vacancies available for certain studies
# of the University of Twente. For each of the certain studies (9 in total) we came up with four job names (keywords) to search 
# for available vacancies related to study and the field of work.

# Variables in order to create the correct output files.
opleiding = "Chemical Engineering"
globalTag = "Process technology wo"
outputdir = "CrawlerResults//MonsterboardResults//" + opleiding +  "//" + globalTag + ".json"

class QuotesSpider(scrapy.Spider):
    name = "provincesMonsterboard"
    
    # Function that greates a request for each page located in the corresponding study / vacancy json URL file. 
    def start_requests(self):
        # Name of the study
        global globalTag
        # Based on the json files created (monsterboardUrlGenerator.py) for monsterboard all the URL's (pages with results) are
        # scraped.  
        urls = json.load(open('CrawlerResults/urls/' + globalTag + '.json'))
        for url in urls:
            yield scrapy.Request(url=url['url'], callback=self.parse)

    def parse(self, response):
        # Province variable to store the province of a vacancy
        province = response.xpath('//input[contains(@placeholder,"Locatie")]/@value').extract()
        # List with all the titles from the vacancies
        titles = response.xpath('//div[contains(@class,"jobTitle")]/h2/a/text()').extract()  
        # Monsterboard page header containing the number of results per page
        header = response.xpath('//h2[contains(@class,"page-title visible-xs")]/text()').extract()
        if len(header) == 0:
            header.append("empty")
        headerList = [int(s) for s in header[0].split() if s.isdigit()]
        numberResult = headerList[0] if len(headerList) > 0 else 0 
        url = response.url
        pageNumber = url.split("page=")
        self.logger.info("Jobtitle size = " + str(len(titles)))

        for i in range(0,len(titles)):
            if numberResult > 0:
                yield {
                    'reportedResults': numberResult,
                    'jobSearch': globalTag,
                    'jobTitle': titles[i],
                    'location': "unkown",
                    'province': province[0],
                    'pageNumber': pageNumber[1]
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