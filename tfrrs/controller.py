#! usr/bin/#!/usr/bin/env python
#This is the controller
#By Matthew and Nick

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from view import *

def main():
    pass

def initial_scrape():
    process = CrawlerProcess(get_project_settings())
    process.crawl('testRunner')
    process.start() # the script will block here until the crawling is finished

if __name__ == '__main__':
    main()
