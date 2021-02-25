# ncaa_db_queries
# queries for getting information from the database

import sqlite3

class DB:

    def __init__(self, name = "ncaa.db"):
        self.name = name
        self.sprints = [55,60,100,110,200,300,400]

    def _start_connection(self):
        try:
            self.conn = sqlite3.connect(self.name)
            self.curr = self.conn.cursor()
        except:
            print('did not connect')

    def _close_connection(self):
        self.conn.close()

    def get_div_teams(self, division, gender):
        """ returns a list of team name and id tuples in a particular division and gender
            input:  division: integer value of 1,2, or 3, gender string of m or f
            output: list of tuples (name, id)
        """
        self._start_connection()
        teams = self.curr.execute("""SELECT name, college_id
                                    FROM Colleges
                                    WHERE division = ? AND gender = ?""",
                                    (division, gender))
        teams = teams.fetchall()
        return teams

    def get_team_roster(self, team_id):
        self._start_connection()
        roster = self.curr.execute("""SELECT (first_name || ' ' || last_name) as name, athlete_id
                                FROM Athletes
                                WHERE college_id = ?""",
                                 (team_id,))
        roster = roster.fetchall()
        self._close_connection()
        return roster

    def get_athlete_seasons(self, athlete_id):
        self._start_connection()
        events = self.curr.execute("""SELECT DISTINCT season
                                        FROM Performances
                                        WHERE athlete_id = ?""",
                                        (athlete_id,)
                                )
        seasons = seasons.fetchall()
        self._close_connection()
        return self._tuplist_to_list(seasons)

    def get_athlete_season_events(self, athlete_id, season):
        self._start_connection()
        events = self.curr.execute("""SELECT event_name
                                      FROM Performances
                                      WHERE athlete_id = ? AND season = ?""", (
                                      athlete_id, season
                                   ))
        events = events.fetchall()
        self._close_connection()
        return self._tuplist_to_list(events)

    def get_athlete_results(self,athlete_id,event_name,season):
        self._start_connection()
        perfomances = self.curr.execute("""SELECT min,sec_or_meters,wind_legal2,wind_legal4,day,month,year
                                          FROM Performances
                                          WHERE athlete_id = ? AND event_name = ? AND season = ?""", (
                                                athlete_id,
                                                event_name,
                                                season
                                        ))
        performances = performances.fetchall()
        units = self.curr.execute("""SELECT DISTINCT time_or_dist FROM Performances
                                     WHERE athlete_id = ? AND event_name = ? AND season = ?""", (
                                           athlete_id,
                                           event_name,
                                           season
                                  )).fetchall()[0][0]
        marks = []
        dates = []
        wind2 = []
        wind4 = []
        if units == 'dist':
            units = 'meters'
            for min, meters, windL2, windL4, day, month, year in performances:
                marks.append(meters)
                wind2.append(windL2)
                wind4.append(windL4)
                dates.append(self._date_to_to_dayssince2000(day,month,year))
        elif int(event_name.split(' ')[0]) in sprints:
            units = 'seconds'
            for min, seconds, windL2, windL4, day, month, year in performances:
                marks.append(self.to_seconds(min,seconds))
                wind2.append(windL2)
                wind4.append(windL4)
                dates.append(self._date_to_to_dayssince2000(day,month,year))
        else:
            units = 'minutes'
            for min, seconds, windL2, windL4, day, month, year in performances:
                marks.append(self.to_minutes(min,seconds))
                wind2.append(windL2)
                wind4.append(windL4)
                dates.append(self._date_to_to_dayssince2000(day,month,year))

        return marks,dates,units,wind2,wind4

    def _tuplist_to_list(self, tuplist):
        return [item for tup in tuplist for item in tup]

    def _date_to_to_days_since2000(self,day,month,year):
        monthdays = [0,31,59,90,120,151,181,212,243,273,304,334]
        leap_year = year%4 == 0 and (year%100 != 0 or year%400 == 0)
        year = year - 2000
        year_days = year*365 + year//4 - year//100 + year//400 +1
        days = year_days + monthdays[month] + day
        if leap_year and month <= 1:
            days -= 1
        return days


    def to_seconds(self,min,seconds):
        if min is not None:
            return min*60 + seconds
        return seconds

    def to_minutes(self,min,seconds):
        return min + seconds/60
