import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    globalTag = ""



    def start_requests(self):
        provinces = ["groningen","friesland","drenthe","overijssel","flevoland","gelderland","utrecht","noord-holland","zuid-holland","zeeland","noord-brabant","limburg"]
        global globalTag
        url = 'http://www.indeed.nl/'
        tag = getattr(self,'tag',None)
        globalTag = tag
        tags = tag.split(" ")
        for i in range(0,len(tags)-1):
            tag = tags[i] + "+"
            tags[i] = tag
        tags.append("vacatures-in")
        for i in tags:
            url += str(i)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(str(self))
        vacature = response.css('.result')[0]
        titles = vacature.xpath('//h2[contains(@class, "jobtitle")]/a/@title').extract()
        locations = vacature.xpath('//div[contains(@data-tn-component, "organicJob")]/span[contains(@class, "location")]/text()').extract()
        #companies = vacature.xpath('//div[contains(@data-tn-component, "organicJob")]/span[contains(@class, "company")]/text()').extract()
        for i in range(0,len(titles)):
            #print("list size: " + str(len(titles)) + "locations size: " + str(len(locations)) + "companies size: " + str(len(companies)))
            yield {
                'jobSearch': globalTag,
                'jobTitle': titles[i],
                'location': locations[i],
        #        'company': companies[i],
            }

        next_page = response.xpath('//span[@class="np" and contains(.,"Volgende")]/../../@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
