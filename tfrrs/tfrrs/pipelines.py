# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .items import TeamItem, AthleteItem, PerformanceItem

import sqlite3


class TfrrsPipeline:

    def __init__(self):
        self.create_connnection()
        self.create_col_table()
        self.create_athlete_table()
        self.create_performance_table()

    def create_connnection(self):
        self.conn = sqlite3.connect("ncaa.db")
        self.curr = self.conn.cursor()

    def close_spider(self,spider):
        self.close_connection()

    def create_col_table(self):
        # dropping table for now
        self.curr.execute("""DROP TABLE IF EXISTS Colleges""")
        self.curr.execute("""CREATE TABLE Colleges(
                            college_id TEXT,
                            name TEXT,
                            division INTEGER,
                            gender TEXT,
                            PRIMARY KEY (college_id)
                            )""")
        self.conn.commit()

    def create_athlete_table(self):
        # dropping table for now
        self.curr.execute("""DROP TABLE IF EXISTS Athletes""")
        self.curr.execute("""CREATE TABLE Athletes(
                            athlete_id INTEGER,
                            first_name TEXT,
                            last_name TEXT,
                            college_id TEXT,
                            PRIMARY KEY (athlete_id),
                            FOREIGN KEY (college_id)
                                REFERENCES Colleges (college_id)
                            )""")

    def create_performance_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS Performances""")
        self.curr.execute("""CREATE TABLE Performances(
                            athlete_id INTEGER,
                            event_name TEXT,
                            minutes INTEGER,
                            sec_or_meters REAL,
                            time_or_dist TEXT,
                            wind_legal2 INTEGER,
                            wind_legal4 INTEGER,
                            day INTEGER,
                            month INTEGER,
                            year INTEGER,
                            season TEXT,
                            UNIQUE(athlete_id,event_name,day,month,year,sec_or_meters)
                            )""")
        self.conn.commit()

    def process_item(self, item, spider):
        if isinstance(item, TeamItem):
            self.store_college(item)
        elif isinstance(item, AthleteItem):
            self.store_athlete(item)
        elif isinstance(item, PerformanceItem):
            self.store_performance(item)
        return item

    def store_college(self, item):
        try:
            self.curr.execute("""INSERT INTO Colleges VALUES(?,?,?,?)""",(
                                item['college_id'],
                                item['name'],
                                item['division'],
                                item['gender']
                            ))
            self.conn.commit()
        except sqlite3.Error() as e:
            self.log_error(e)
        except sqlite3.IntegrityError() as e:
            self.log_error(e)


    def store_athlete(self, item):
        try:
            self.curr.execute("""INSERT INTO Athletes VALUES(?,?,?,?)""", (
                                item['athlete_id'],
                                item['first_name'],
                                item['last_name'],
                                item['college_id']
                            ))
            self.conn.commit()
        except sqlite3.Error() as e:
            self.log_error(e)
        except sqlite3.IntegrityError() as e:
            self.log_error(e)

    def store_performance(self, item):
        try:
            self.curr.execute("""INSERT INTO Performances VALUES(?,?,?,?,?,?,?,?,?,?,?)""", (
                                item['athlete_id'],
                                item['event_name'],
                                item['min'],
                                item['sec_or_meters'],
                                item['time_or_dist'],
                                item['wind_legal2'],
                                item['wind_legal4'],
                                item['day'],
                                item['month'],
                                item['year'],
                                item['season']
                            ))
            self.conn.commit()
        except sqlite3.Error() as e:
            self.log_error(e)
        except sqlite3.IntegrityError() as e:
            self.log_error(e)

    def log_error(self, error):
        with open("sql_error_log.txt", 'a') as f:
            f.write(error)

    def close_connection(self):
        self.conn.close()
