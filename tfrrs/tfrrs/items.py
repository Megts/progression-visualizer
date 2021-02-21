# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TeamItem(scrapy.Item):
    # define the fields for your item here like:
    college_id = scrapy.Field()
    name = scrapy.Field()
    division = scrapy.Field()
    gender = scrapy.Field()

class AthleteItem(scrapy.Item):
    athlete_id = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    college_id = scrapy.Field()



class PerformanceItem(scrapy.Item):
    athlete_id = scrapy.Field()
    event_name = scrapy.Field()
    min = scrapy.Field()
    sec_or_meters = scrapy.Field()
    time_or_dist = scrapy.Field()
    wind_legal2 = scrapy.Field()
    wind_legal4 = scrapy.Field()
    day = scrapy.Field()
    month = scrapy.Field()
    year = scrapy.Field()
    season = scrapy.Field()
