# ncaa_db_queries
# queries for getting information from the database

import sqlite3
from datetime import datetime, MINYEAR

class DB:

    def __init__(self, name = "ncaa.db"):
        self.name = name
        sprints = [55,60,100,110,200,300,400]
        self.sprints = []
        for sprint in sprints:
            self.sprints.append(str(sprint) + ' Meters')
            self.sprints.append(str(sprint) + ' Hurdles')



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

    def get_ahtlete_name(self, athlete_id):
        self._start_connection()
        name = self.curr.execute("""SELECT first_name, last_name
                                    FROM Athletes WHERE athlete_id = ?""",
                                    (athlete_id,)).fetchall()
        self._close_connection()
        return name[0][0] + ' ' + name[0][1]

    def get_athlete_seasons(self, athlete_id):
        self._start_connection()
        seasons = self.curr.execute("""SELECT DISTINCT season
                                        FROM Performances
                                        WHERE athlete_id = ?""",
                                        (athlete_id,)
                                )
        seasons = seasons.fetchall()
        self._close_connection()
        return self._tuplist_to_list(seasons)

    def get_athlete_season_events(self, athlete_id, season):
        self._start_connection()
        events = self.curr.execute("""SELECT DISTINCT event_name
                                      FROM Performances
                                      WHERE athlete_id = ? AND season = ?""", (
                                      athlete_id, season
                                   ))
        events = events.fetchall()
        self._close_connection()
        return self._tuplist_to_list(events)

    def get_athlete_results(self,athlete_id,event_name,season):
        print(athlete_id,event_name,season)
        self._start_connection()
        performances = self.curr.execute("""SELECT min,sec_or_meters,wind_legal2,wind_legal4,day,month,year
                                          FROM Performances
                                          WHERE athlete_id = ? AND event_name = ? AND season = ?
                                          ORDER BY year, month, day""", (
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
                                  ))
        units = units.fetchall()
        units = units[0][0]
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
                dates.append(date(year,month+1,day))
        else:
            units = 'time'
            for min, seconds, windL2, windL4, day, month, year in performances:
                if seconds is not None:
                    sec = int(seconds)
                    micro = int((seconds-sec) * 10**6)
                    if min is None:
                        min = 0
                    marks.append(datetime(3,3,15,minute=min,second=sec,microsecond=micro))
                else:
                    marks.append(None)
                wind2.append(windL2)
                wind4.append(windL4)
                dates.append(datetime(year,month + 1,day))

        return marks,dates,units,wind2,wind4

    def _tuplist_to_list(self, tuplist):
        return [item for tup in tuplist for item in tup]

    def to_seconds(self,min,seconds):
        if seconds is not None:
            if min is not None:
                    return min*60 + seconds
            return seconds
        return None

    def to_minutes(self,min,seconds):
        if min is not None:
            return min + seconds/60
        return None
