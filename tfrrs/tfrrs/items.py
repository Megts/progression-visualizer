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
    name = scrapy.Field()
    college_id = scrapy.Field()



class PerformanceItem(scrapy.Item):
    athlete_id = scrapy.Field()
    event_name = scrapy.Field()
    mark = scrapy.Field()
    day = scrapy.Field()
    month = scrapy.Field()
    year = scrapy.Field()
    season = scrapy.Field()
