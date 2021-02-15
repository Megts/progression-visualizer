# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3


class TfrrsPipeline:

    def __init__(self):
        self.create_connnection()
        self.create_col_tab()
        self.create_athlete_tab()
        self.create_performance_tab()

    def create_connnection(self):
        self.conn = sqlite3.connect("ncaa.db")
        self.curr = self.conn.cursor()

    def create_col_tab(self):
        # dropping table for now
        self.curr.execute("""DROP TABLE IF EXISTS Colleges""")
        self.curr.execute("""CREATE TABLE Colleges(
                            college_id INTEGER,
                            name TEXT,
                            division INTEGER,
                            gender TEXT,
                            PRIMARY KEY (college_id)
                            )""")

    def create_athlete_tab(self):
        # dropping table for now
        self.curr.execute("""DROP TABLE IF EXISTS Athletes""")
        self.curr.execute("""CREATE TABLE Athletes(
                            athlete_id INTEGER,
                            name TEXT,
                            college_id INTEGER,
                            PRIMARY KEY (athlete_id),
                            FOREIGN KEY (college_id)
                                REFERENCES Colleges (college_id)
                            )""")

    def create_performance_tab(self):
        self.curr.execute("""DROP TABLE IF EXISTS Performances""")
        self.curr.execute("""CREATE TABLE Performances(
                            athlete_id INTEGER,
                            event_name TEXT,
                            mark TEXT,
                            date TEXT,
                            venue TEXT,
                            season TEXT,
                            UNIQUE(athlete_id,event_name,date,mark)
                            )""")

    def process_college(self, item, spider):
        return item

    def store_college(self, item):
        pass

    def process_athlete(self, item, spider):
        pass

    def store_athlete(self, item):
        pass

    def process_performance(self, item, spider):
        pass

    def store_performance(self, item):
        pass

    def close_connection(self):
        self.conn.close()
