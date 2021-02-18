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
        try:
            self.conn = sqlite3.connect("ncaa.db")
            self.curr = self.conn.cursor()
        except Sqlite3.Error() as e:
            print("something went wrong", e)

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
                            name TEXT,
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
                            mark TEXT,
                            day INTEGER,
                            month INTEGER,
                            year INTEGER,
                            venue TEXT,
                            season TEXT,
                            UNIQUE(athlete_id,event_name,day,month,year,mark)
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
            self.curr.execute("""INSERT INTO Colleges(college_id,name,division,gender) VALUES(?,?,?,?)""",(
                                item['college_id'],
                                item['name'],
                                item['division'],
                                item['gender']
                            ))
            self.conn.commit()
            print('succesfully saved:', item['college_id'],item['name'], item['division'],item['gender'])
        except sqlite3.Error() as e:
            print(e)


    def store_athlete(self, item):
        try:
            self.curr.execute("""INSERT INTO Athletes(athlete_id,name,college_id) VALUES(?,?,?)""", (
                                item['athlete_id'],
                                item['name'],
                                item['college_id']
                            ))
            self.conn.commit()
            print('succesfully saved:', item)
        except sqlite3.Error() as e:
            print(e)

    def store_performance(self, item):
        self.curr.execute("""INSERT INTO Performances VALUES(?,?,?,?,?,?,?,?)""", (
                            item['athlete_id'],
                            item['event_name'],
                            item['mark'],
                            item['day'],
                            item['month'],
                            item['year'],
                            item['venue'],
                            item['season']
                        ))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
