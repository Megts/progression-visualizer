# testing scrapy to get used to it

import scrapy
from ..items import TeamItem, AthleteItem, PerformanceItem

# Example spider
class TFRRSspider(scrapy.Spider):
    name = "testRunner"

    allowed_domains = ['tfrrs.org']

    start_urls = ['https://tfrrs.org/leagues/49.html',]
                  #'https://tfrrs.org/leagues/50.html',
                  #'https://tfrrs.org/leagues/51.html',]

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_team_athletes)

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
        for i in range(len(teamLink)):
            team = TeamItem()
            name = teamName[i]
            try:
                team_id = teamLink[i].split('/')[-1].replace('.html', '')
                gender = teamLink[i].split('/')[-1].split('_')[2]
                team['college_id'] = team_id
                team['name'] = name
                team['division'] = division
                team['gender'] = gender

                yield team
                yield response.follow(teamLink[i], callback=self.parse_team_athletes)
            except IndexError:
                print(name, "does not follow the normal url schema and was not added")


    def parse_team_athletes(self, response):
        print('parsing team')
        athName = response.xpath('//div[@class="col-lg-4 "]/table//a/text()').getall()
        athLink = response.xpath('//div[@class="col-lg-4 "]/table//a/@href').getall()
        team_id = response.url.split('/')[-1].replace('.html', '')
        print('entering loop')
        print(len(athLink))
        for i in range(len(athLink)):
            athlete = AthleteItem()
            name = athName[i]
            splitLink = athLink[i].split('/')
            athID = splitLink[-3]

            athlete['athlete_id'] = athID
            athlete['name'] = name
            athlete['college_id'] = team_id
            print(athlete)
            yield athlete


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
                day, month, year = date_to_tup(date)
                perf['ahtlete_id'] = athlete_id
                perf['event_name'] = event_name
                perf['mark'] = mark
                perf['day'] = day
                per['month'] = month
                perf['year'] = year
                perf['venue'] = venue
                perf['season'] = season

                yield perf


    def cleanTable(table):
        newTable =[]
        for line in table:
            line = line.replace('\n', '').replace(' ', '')
            if line != '':
                if line[:3] != 'Top':
                    if len(newTable[-1]) < 3:
                        newTable[-1].append(line)
                    else:
                        newTable.append([line])
        return newTable

    def date_to_tup(date):
        months = {'jan':0, 'feb':1, 'mar':2, 'apr':3, 'may':4,
                    'jun':5, 'jul':6, 'aug':7, 'sep':8, 'oct':9,
                    'nov':10, 'dec':11}
        month_day, year = date.split(',')
        month_day = month_day.split('-')
        month, day = month_day[0].split[' ']
        month = months[month.lower()]
        return int(day), int(month), int(year)
