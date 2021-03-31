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
            division = 1
        if league == '50.html':
            division = 2
        if league == '51.html':
            division = 3
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
                female_team['name'] = f_col_name
                female_team['division'] = division
                female_team['gender'] = 'f'

                yield female_team
                yield response.follow(f_col_link, callback=self.parse_team_athletes)


    def parse_team_athletes(self, response):
        athName = response.xpath('//div[@class="col-lg-4 "]/table//a/text()').getall()
        athLink = response.xpath('//div[@class="col-lg-4 "]/table//a/@href').getall()
        team_id = response.url.split('/')[-1].replace('.html', '')
        if len(athLink) == 0:
            athName = response.xpath('//div[@class="col-lg-4"]/table//a/text()').getall()
            athLink = response.xpath('//div[@class="col-lg-4"]/table//a/@href').getall()
            if len(athLink) == 0:
                self.log_error(team_id + " has no roster, or the the class is really messed up\n")
        for i in range(len(athLink)):
            athlete = AthleteItem()
            name = athName[i]
            last_name, first_name = name.split(',')
            last_name = last_name.strip()
            first_name = first_name.strip()
            splitLink = athLink[i].split('/')
            athID = int(splitLink[-3])

            athlete['athlete_id'] = athID
            athlete['first_name'] = first_name
            athlete['last_name'] = last_name
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
                mark, units, wind_legal2, wind_legal4 = self.parse_mark(mark)
                if sec_or_meters is not None:
                    perf['athlete_id'] = athlete_id
                    perf['event_name'] = event_name
                    perf['mark'] = mark
                    perf['units'] = units
                    perf['wind_legal2'] = wind_legal2
                    perf['wind_legal4'] = wind_legal4
                    perf['day'] = day
                    perf['month'] = month
                    perf['year'] = year
                    perf['season'] = season

                    yield perf


    def date_to_tup(self, date):
        months = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5,
                    'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10,
                    'nov':11, 'dec':12}
        month_day, year = date.split(',')
        month_day = month_day.split('-')
        month, day = month_day[0].strip().replace('  ', ' ').split(' ')
        month = months[month.lower()]
        return int(day), int(month), int(year)


    def parse_mark(self, mark):
        wind_legal2 = 1
        wind_legal4 = 1

        if mark in ['ND', 'NT', 'NH', 'DNF', 'FOUL', 'DNS', 'DQ']:
            return [None for i in range(5)]
        if 'm' in sec_or_meters:
            time_or_dist = 'Meters'
            mark = mark.replace('m', '')
        elif ':' in mark:
            units = 'Time'
        elif int(mark) > 60:
            units = 'Points'

        if 'W' in mark:
            sec_or_meters = sec_or_meters.replace('W','')
            wind_legal2 = 0
            wind_legal4 = 0
        elif 'w' in mark:
            sec_or_meters = sec_or_meters.replace('w', '')
            wind_legal2 = 0
        return mark, units wind_legal2, wind_legal4


    def log_error(self, error):
        with open('runner_log.txt', 'a') as f:
            f.write(error)
