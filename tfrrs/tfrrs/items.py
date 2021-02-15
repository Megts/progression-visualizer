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
    gender = srcapy.Field()

class AthleteItem(scrapy.Item):
    athlete_id = scrapy.Field()
    name = scrapy.Field()
    college_id = srapy.Field()



class PerfomanceItem(scrapy.Item):
    athlete_id = srapy.Field()
    event_name = srapy.Field()
    mark = srapy.Field()
    date = srapy.Field()
    venue = srapy.Field()
    season = srapy.Field()
