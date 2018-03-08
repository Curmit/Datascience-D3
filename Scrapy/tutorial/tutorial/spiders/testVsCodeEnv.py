import scrapy
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = "provinces"
    globalTag = ""


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
        # Start url
        url = 'http://www.indeed.nl/'
        # Getting the tags from the input parameters
        tag = "Data Science"
        # Globaltag is set to be able to add it to output file
        globalTag = tag
        # Tags are split i.e. "Data Scientist" gets split to build url
        tags = tag.split(" ")
        # "-" are added to indivitual tags for URL builder
        for i in range(len(tags)):
            tag = tags[i] + "-"
            tags[i] = tag

        tags.append("vacatures-in-")
        # Correct url's are build format: "http://www.indeed.nl/data-scientist-vacatures-in-overijssel"
        # For each province there is a request done and the spider crawls the page
        for province in provinces:
            url = 'http://www.indeed.nl/'
            for i in tags:
                url += str(i)
            url += province
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(str(self))
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


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(QuotesSpider)
process.start() # the script will block here until the crawling is finished