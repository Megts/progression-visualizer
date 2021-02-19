# testing scrapy to get used to it

import scrapy
from ..items import TeamItem, AthleteItem, PerformanceItem

# Example spider
class TFRRSspider(scrapy.Spider):
    name = "testRunner"

    allowed_domains = ['tfrrs.org']

    start_urls = ['https://tfrrs.org/leagues/49.html',
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
        rows = response.xpath('//div[@class="col-lg-4"]/table/tbody/tr')
        for row in rows:
            male_team = TeamItem()
            female_team = TeamItem()
            m_col, f_col = row.xpath('.//td')
            m_col_link = m_col.xpath('./a/@href').get()
            m_col_name = m_col.xpath('./a/text()').get()
            if m_col_link is not None:
                team_id = m_col_link.split('/')[-1].replace('.html', '')
                male_team['college_id'] = team_id
                male_team['name'] = m_col_name
                male_team['division'] = division
                male_team['gender'] = 'm'

                yield male_team
                yield response.follow(m_col_link, callback=self.parse_team_athletes)
            f_col_link = f_col.xpath('./a/@href').get()
            f_col_name = f_col.xpath('./a/text()').get()
            if f_col_link is not None:
                team_id = f_col_link.split('/')[-1].replace('.html', '')
                female_team['college_id'] = team_id
                female_team['name'] = m_col_name
                female_team['division'] = division
                female_team['gender'] = 'f'

                yield female_team
                yield response.follow(f_col_link, callback=self.parse_team_athletes)


    def parse_team_athletes(self, response):
        athName = response.xpath('//div[@class="col-lg-4 "]/table//a/text()').getall()
        athLink = response.xpath('//div[@class="col-lg-4 "]/table//a/@href').getall()
        team_id = response.url.split('/')[-1].replace('.html', '')
        if len(athLink) == 0:
            self.log_error(team_id + " has no roster, or the \"col-lg-4 \" may not hav a space at end")
        for i in range(len(athLink)):
            athlete = AthleteItem()
            name = athName[i]
            last_name, first_name = name.split(',')
            last_name = last_name.strip()
            first_name = first_name.strip()
            splitLink = athLink[i].split('/')
            athID = splitLink[-3]

            athlete['athlete_id'] = athID
            athlete['name'] = name
            athlete['college_id'] = team_id
            yield athlete
            yield response.follow(athLink[i], callback=self.parse_athlete_events)


    def parse_athlete_events(self, response):
        athlete_id = response.url.split('/')[-3]
        eventTables = response.xpath('//div[@id="event-history"]/table//tr')
        perf = PerformanceItem()
        for line in eventTables:
            line = line.xpath('.//text()').getall()
            line = [td.replace('\n', '').replace('\t\t', ',') for td in line]
            i = 0
            while i < len(line):
                if '' == line[i].strip():
                    line.pop(i)
                else:
                    i += 1
            if len(line) ==2:
                event_name, season = line[0].split(", ")
                event_name = event_name.strip()
                season = season.strip(' ()')
            else:
                mark = line[0]
                date = line[-1]
                day, month, year = self.date_to_tup(date)

                perf['athlete_id'] = athlete_id
                perf['event_name'] = event_name
                perf['mark'] = mark
                perf['day'] = day
                perf['month'] = month
                perf['year'] = year
                perf['season'] = season

                yield perf

    def date_to_tup(self, date):
        months = {'jan':0, 'feb':1, 'mar':2, 'apr':3, 'may':4,
                    'jun':5, 'jul':6, 'aug':7, 'sep':8, 'oct':9,
                    'nov':10, 'dec':11}
        month_day, year = date.split(',')
        month_day = month_day.split('-')
        month, day = month_day[0].strip().replace('  ', ' ').split(' ')
        month = months[month.lower()]
        return int(day), int(month), int(year)
