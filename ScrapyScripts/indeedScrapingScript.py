import scrapy
from scrapy.crawler import CrawlerProcess

# CREATED BY:
# Carmen Burghardt (Master student Creative Technology @ University of Twente)
# Rick Lenderink (Master student Business Information Technology @ University of Twente)
# 
# 
# Scraping script designed for http://wwww.indeed.nl/ in order to get, given a certain jobsearch + province, 
# the job title and job location. 
# 
# This information is used to give a visual representation of the amount of vacancies available for certain studies
# of the University of Twente. For each of the certain studies (9 in total) we came up with four job names (keywords) to search 
# for available vacancies related to study and the field of work.

# Variables in order to create the correct output files.
opleiding = "Mechanical Engineering"
globalTag = "Product Ingenieur wo"
outputdir = "CrawlerResults//IndeedResults//"+ str(opleiding) +"//" + str(globalTag) + ".json"

class QuotesSpider(scrapy.Spider):
    name = "provincesIndeed"
    
    # Function that generates a URL for all provinces given a jobSearch
    # a job search is divided into multiple tasks per province since its seems that
    # Indeed has a limit of showing approximately 1000 vacancies when a search doesn't 
    # include a location.
    # Url's are build in format: "http://www.indeed.nl/data-scientist-vacatures-in-overijssel"
    def start_requests(self):
        provinces = ["groningen",\
                    "friesland",\
                    "drenthe",\
                    "overijssel",\
                    "flevoland",\
                    "gelderland",\
                    "utrecht",\
                    "noord-holland",\
                    "zuid-holland",\
                    "zeeland",\
                    "noord-brabant",\
                    "limburg"]
        global globalTag
        global opleiding
        # Start url
        url = 'http://www.indeed.nl/'
        # Tags are split i.e. "Data Scientist" gets split to build url
        tags = globalTag.split(" ")
        # "-" are added to indivitual tags for URL builder
        for i in range(len(tags)):
            tag = tags[i] + "-"
            tags[i] = tag
        tags.append("vacatures-in-")
        # For each province there is a request done and the spider crawls the page
        for province in provinces:
            url = 'http://www.indeed.nl/'
            for i in tags:
                url += str(i)
            url += province
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    # Page crawler, crawls a given page
    def parse(self, response):
        # HTML vacancy element containing details about a vacancy
        vacature = response.css('.result')[0]
        # Title element comming from a vacancy, contains Xpath to the jobTitle
        titles = vacature.xpath('//h2[contains(@class, "jobtitle")]/a/@title').extract()
        # Location of a vacancy (i.e. city, province or area)
        locations = vacature.xpath('//div[contains(@data-tn-component, "organicJob")]/span[contains(@class, "location")]/text()').extract()
        # Province variable to store the province of a vacancy
        province = response.xpath('//input[contains(@name,"l") and contains(@class,"input_text")]/@value').extract()
        for i in range(0,len(titles)):
            yield {
                'jobSearch': globalTag,
                'jobTitle': titles[i],
                'location': locations[i],
                'province': province[0]
            }
        # Next page build in function from Scrapy which goes to the next page if there is one
        next_page = response.xpath('//span[@class="np" and contains(.,"Volgende")]/../../@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'FEED_URI': outputdir
})

process.crawl(QuotesSpider)
process.start() # the script will block here until the crawling is finished