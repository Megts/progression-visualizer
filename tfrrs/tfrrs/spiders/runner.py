# testing scrapy to get used to it

import scrapy

# Example spider
class TFRRSspider(scrapy.Spider):
    name = "runner"

    def start_requests(self):
        urls = ["https://www.tfrrs.org/leagues/48.html"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        filename = 'NCAA_teams.csv'
        with open(filename, 'w') as f:
            teamName = response.xpath('//div[@class="col-lg-4"]/table/tbody//a/text()').getall()
            teamLink = response.xpath('//div[@class="col-lg-4"]/table/tbody//a/@href').getall()
            for i in range(len(teamName)):
                f.write(teamName[i] + "," + teamLink[i] +'\n')
        self.log('Saved file as %s' % filename)
