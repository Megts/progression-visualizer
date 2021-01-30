# testing scrapy to get used to it

import scrapy

# Example spider
class TFRRSspider(scrapy.Spider):
    name = "runner"

    def start_requests(self):
        urls = ["https://www.tfrrs.org/athletes/6592815/Wartburg/Joe_Freiburger"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        filename = response.url.split("/")[-2] + '.' + response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file as %s' % filename)
