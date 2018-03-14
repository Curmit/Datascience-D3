import scrapy
import math as mt

# HOW TO RUN:
# 
# scrapy crawl provincesMonsterboard -o 'outputfilename'.json -a tag="vacaturenaam"
#
# baseurl:
# data scientist
# https://www.monsterboard.nl/vacatures/zoeken/data-scientist_5?where=Noord__2DHolland&cy=nl
# 
# boekhouder
# https://www.monsterboard.nl/vacatures/zoeken/boekhouder_5?where=Noord__2DHolland&cy=nl
#
# Get jobtitles
# response.xpath('//div[contains(@class,"jobTitle")]/h2/a/text()').extract()  
#
# Get jobLocations
#  response.xpath('//div[contains(@class,"job-specs-location")]/p/a/text()').extract()
#
# Get Province
#  response.xpath('//input[contains(@placeholder,"Locatie")]/@value').extract()
# 
# 25 results per page, divider is reported result divided by 25 for the number of pages
# eventhough the actual results are much less than the reported number of results
# page url:
# https://www.monsterboard.nl/vacatures/zoeken/boekhouder_5?where=Noord__2DHolland&cy=nl&page=22
# 
# number of vacancies
# response.xpath('//h2[contains(@class,"page-title visible-xs")]/text()').extract()[0]
# 

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
        tag = getattr(self,'tag',None)
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
            response = scrapy.http.TextResponse(url=url)
            header = response.xpath('//h2[contains(@class,"page-title visible-xs")]/text()').extract()
            print(header)
            #yield scrapy.Request(url=url, callback=self.parse)

    

    def parseTwo(self, response):
        vacature = response.css('.result')[0]
        titles = vacature.xpath('//h2[contains(@class, "jobtitle")]/a/@title').extract()
        locations = vacature.xpath('//div[contains(@data-tn-component, "organicJob")]/span[contains(@class, "location")]/text()').extract()
        province = response.xpath('//input[contains(@name,"l") and contains(@class,"input_text")]/@value').extract()
        #companies = vacature.xpath('//div[contains(@data-tn-component, "organicJob")]/span[contains(@class, "company")]/text()').extract()
        for i in range(0,len(titles)):
            #print("list size: " + str(len(titles)) + "locations size: " + str(len(locations)) + "companies size: " + str(len(companies)))
            yield {
                'jobSearch': globalTag,
                'jobTitle': titles[i],
                'location': locations[i],
        #        'company': companies[i],
                'province': province[0]
            }

        next_page = response.xpath('//span[@class="np" and contains(.,"Volgende")]/../../@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
