# testing scrapy to get used to it

import scrapy
from ..items import DivItem, TeamItem, AthleteItem

# Example spider
class TFRRSspider(scrapy.Spider):
    name = "testRunner"

    allowed_domains = ['tfrrs.org']

    start_urls = ['https://tfrss.org/leagues/49.html',
                  'https://tfrrs.org/leagues/50.html',
                  'https://tfrrs.org/leagues/51.html',]


    def parse_div_teams(self, response):
        league = response.url.split("/")[-1]
        if league == '49.html':
            divion = 'DI'
        if league = '50.html':
            division = 'DII'
        if league = '51.html':
            division = 'DIII'
        teamName = response.xpath('//div[@class="col-lg-4"]/table/tbody/tr/td/a/text()').getall()
        teamLink = response.xpath('//div[@class="col-lg-4"]/table/tbody/tr/td/a/@href').getall()
        for link in teamLink:

        self.log('Saved file as %s' % filename)


    def parse_team_athletes(self, response):
        athName = response.xpath('//div[@class="col-lg-4"]/table/tbody/tr/td/a/text()').getall()
        athLink = response.xpath('//div[@class="col-lg-4"]/table/tbody/tr/td/a/@href').getall()


    def parse_athlete_events(self, response):
        athlete_id = response.url
        eventTables = response.xpath('//div[@id="event-history"]/table//text()').getall()
        eventTables = cleanTable(eventTables)
        currentEvent = None
        for line in eventTables:
            if '\t' in line:
                event = line.replace('\t\t', ',')
                event_name, season = event.split(",")




    def cleanTable(table):
        newTable = []
        for line in table:
            line = line.replace('\n', '').replace(' ', '')
            if line != '':
                if line[:3] != 'Top':
                    newTable.append(line)
        return newTable
