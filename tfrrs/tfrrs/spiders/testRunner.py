# testing scrapy to get used to it

import scrapy
from ..items import TeamItem, AthleteItem, PerformanceItem

# Example spider
class TFRRSspider(scrapy.Spider):
    name = "testRunner"

    allowed_domains = ['tfrrs.org']

    start_urls = ['https://tfrss.org/leagues/49.html',
                  'https://tfrrs.org/leagues/50.html',
                  'https://tfrrs.org/leagues/51.html',]

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_div_teams)

    def parse_div_teams(self, response):
        league = response.url.split("/")[-1]
        if league == '49.html':
            division = 'DI'
        if league == '50.html':
            division = 'DII'
        if league == '51.html':
            division = 'DIII'
        teamName = response.xpath('//div[@class="col-lg-4"]/table/tbody/tr/td/a/text()').getall()
        teamLink = response.xpath('//div[@class="col-lg-4"]/table/tbody/tr/td/a/@href').getall()
        team = TeamItem()
        for i in range(len(teamLink)):
            name = teamName[i]
            try:
                team_id = '_'.join(teamLink[i].split('/')[-1].split('.')[0].split('_')[3:])
                gender = teamLink[i].split('/')[-1].split('_')[2]
            except e:
            team['college_id'] = team_id + gender
            team['name'] = name
            team['division'] = division
            team['gender'] = gender

            yield team

        for link in teamLink:
            yield response.follow(link, callback=self.parse_team_athletes)


    def parse_team_athletes(self, response):
        athName = response.xpath('//div[@class="col-lg-4"]/table/tbody/tr/td/a/text()').getall()
        athLink = response.xpath('//div[@class="col-lg-4"]/table/tbody/tr/td/a/@href').getall()
        athlete = AthleteItem()
        for i in ragnge(len(athLink)):
            name = athName[i]
            splitLink = athLink[i].split('/')
            athID = splitLink[-3]
            teamID = splitLink[-2]

            athlete['athlete_id'] = athID
            athlete['name'] = name
            athlete['college_id'] = teamID


    def parse_athlete_events(self, response):
        athlete_id = response.url.split()[-3]
        eventTables = response.xpath('//div[@id="event-history"]/table//text()').getall()
        eventTables = cleanTable(eventTables)
        currentEvent = None
        perf = PerformanceItem()
        for line in eventTables:
            if '\t' in line:
                event = line.replace('\t\t', ',')
                event_name, season = event.split(",")
                season = season.strip('()')
            else:
                mark, venue, date = line
                perf['ahtlete_id'] = athlete_id
                perf['event_name'] = event_name
                perf['mark'] = mark
                perf['date'] = date
                perf['venue'] = venue
                perf['season'] = season

                yield perf

    def cleanTable(table):
        newTable = []
        for line in table:
            line = line.replace('\n', '').replace(' ', '')
            if line != '':
                if line[:3] != 'Top':
                    if len(newTable[-1]) < 3:
                        newTable[-1].append(line)
                    else:
                        newTable.append([line])
        return newTable
