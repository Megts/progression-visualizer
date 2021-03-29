# ncaa_db_queries
# queries for getting information from the database

import sqlite3
from numpy import datetime64, timedelta64

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
                                    WHERE division = ? AND gender = ?
                                    ORDER BY name""",
                                    (division, gender))
        teams = teams.fetchall()
        return teams

    def get_init_team_roster(self, team_id):
        self._start_connection()
        cmd = f"""SELECT (first_name || ' ' || last_name) as name, athlete_id
                                FROM Athletes
                                WHERE college_id = {team_id!r}
                                ORDER BY name"""
        roster = self.curr.execute(cmd)
        roster = roster.fetchall()
        self._close_connection()
        return roster

    def get_remaining_team_roster(self, team_id, athlete_ids, season, event):
        self._start_connection()
        ath_ids = str(athlete_ids).replace('[',"(").replace(']',')')
        cmd = f"""SELECT (first_name || ' ' || last_name) as name, a.athlete_id
                                FROM Athletes as a
                                INNER JOIN (SELECT DISTINCT season, event_name, p.athlete_id
                                            FROM Performances as p) as perf
                                ON a.athlete_id = perf.athlete_id
                                WHERE college_id = {team_id!r} AND a.athlete_id NOT IN {ath_ids}
                                AND perf.season = {season!r} AND perf.event_name = {event!r}
                                ORDER BY name"""
        roster = self.curr.execute(cmd)
        roster = roster.fetchall()
        self._close_connection()
        return roster

    def get_ahtlete_name(self, athlete_id):
        self._start_connection()
        name = self.curr.execute("""SELECT (first_name || ' ' || last_name) as name
                                    FROM Athletes WHERE athlete_id = ?""",
                                    (athlete_id,)).fetchall()
        self._close_connection()
        return name[0][0]

    def get_athlete_seasons(self, athlete_id):
        self._start_connection()
        seasons = self.curr.execute("""SELECT DISTINCT season
                                        FROM Performances
                                        WHERE athlete_id = ?
                                        ORDER BY season""",
                                        (athlete_id,)
                                )
        seasons = seasons.fetchall()
        self._close_connection()
        return self._tuplist_to_list(seasons)

    def get_athletes_overlaping_seasons(self,athlete_ids):
        self._start_connection()
        tables_to_intersect = []
        cmd = """SELECT u.season FROM ( """
        for i in range(len(athlete_ids)):
            cmd += f"""SELECT season FROM Performances WHERE athlete_id = {athlete_ids[i]}"""
            if i < len(athlete_ids)-1:
                cmd += """ INTERSECT """
        cmd += """) as u ORDER BY u.season"""
        seasons = self.curr.execute(cmd)
        seasons = seasons.fetchall()
        self._close_connection()
        return self._tuplist_to_list(seasons)

    def get_athlete_season_events(self, athlete_id, season):
        self._start_connection()
        events = self.curr.execute("""SELECT DISTINCT event_name
                                      FROM Performances
                                      WHERE athlete_id = ? AND season = ?
                                      ORDER BY event_name""", (
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
        units = self._get_units(event_name)
        season_year = performances[0][6]
        if performances[0][5] == 11:
            season_year += 1
        year1 = season_year
        completed_seasons = []
        marks = []
        dates = []
        wind2 = []
        wind4 = []
        if units == 'dist':
            units = 'Meters'
            for min, meters, windL2, windL4, day, month, year in performances:
                if season=='Indoor' and (year>season_year or (year==season_year and month>3)):
                    completed_seasons.append([marks,wind2,wind4,dates,season_year])
                    season_year = year
                    if month == 11 and season == 'Indoor':
                        season_year += 1
                    marks = []
                    dates = []
                    wind2 = []
                    wind4 = []
                else:
                    if year > season_year:
                        completed_seasons.append([marks,wind2,wind4,dates, season_year])
                        season_year = year
                        marks = []
                        dates = []
                        wind2 = []
                        wind4 = []
                marks.append(meters)
                wind2.append(windL2)
                wind4.append(windL4)
                dates.append(self._date_to_2000_dt(year,month,day, season_year))
        else:
            units = 'Time'
            for min, seconds, windL2, windL4, day, month, year in performances:

                if season=='XC' and year>season_year and month>3:
                    completed_seasons.append([marks,wind2,wind4,dates,season_year])
                    season_year = year
                    marks = []
                    dates = []
                    wind2 = []
                    wind4 = []
                elif season=='Indoor' and (year>season_year or (year==season_year and month>3)):
                    completed_seasons.append([marks,wind2,wind4,dates,season_year])
                    season_year = year
                    if month == 11 and season == 'Indoor':
                        season_year += 1
                    marks = []
                    dates = []
                    wind2 = []
                    wind4 = []
                else:
                    if year > season_year:
                        completed_seasons.append([marks,wind2,wind4,dates,season_year])
                        season_year = year
                        marks = []
                        dates = []
                        wind2 = []
                        wind4 = []

                if seconds > 100:
                    units = "Points"
                    marks.append(seconds)
                    wind2.append(windL2)
                    wind4.append(windL4)
                    dates.append(self._date_to_2000_dt(year,month,day, season_year))
                else:
                    if seconds is not None:
                        marks.append(self._time_to_dt(min,seconds))
                    else:
                        marks.append(None)
                    wind2.append(windL2)
                    wind4.append(windL4)
                    dates.append(self._date_to_2000_dt(year,month,day, season_year))

        completed_seasons.append([marks,wind2,wind4,dates, season_year])
        return completed_seasons, units

    def _get_units(self, event_name):
        self._start_connection()
        unit = self.curr.execute("""SELECT time_or_dist FROM Performances
                                    WHERE event_name = ?""", (event_name,)).fetchall()
        return unit[0][0]

    def _tuplist_to_list(self, tuplist):
        return [item for tup in tuplist for item in tup]

    def _time_to_dt(self, min,seconds):
        if min is None:
            min = 0
        sec = int(seconds)
        hundreth = int((seconds-sec)*100)
        min = ('0' + str(min))[-2:]
        return datetime64(f'2000-01-01T00:{self._2digs(min)}:{self._2digs(sec)}.{hundreth}')

    def _date_to_2000_dt(self,year,month,day, season_year):
        dt = datetime64(f'{year}-{self._2digs(month+1)}-{self._2digs(day)}')
        td = datetime64(f'{season_year}-01-01')-datetime64('2000-01-01')
        return dt - td

    def _2digs(self, num):
        return ('0' + str(num))[-2:]

    def to_minutes(self,min,seconds):
        if min is not None:
            return min + seconds/60
        return None
#Returns the athletes best time/distance all time
    def get_athlete_pr(self,athlete_id, event_name):
        self._start_connection()
        if self._get_units(event_name) == 'dist':
            order = 'DESC'
        else:
            order = 'ASC'
        pr = self.curr.execute("""SELECT min, sec_or_meters
                                    FROM Performances
                                    WHERE athlete_id = ? AND event_name = ?
                                    ORDER BY min, sec_or_meters ?
                                    Limit 1""",(
                                    athlete_id, event_name, order
                                ))
        pr = pr.fetchall()
        self._close_connection()
        units = self._get_units(event_name)
        pr_min, pr_sec = pr
        if unit == 'dist' or pr_sec > 100:
            pr = pr_sec
        else:
            pr = self._time_to_dt(pr_min, pr_sec)
        return pr
#Returns selected athletes best time/distance in first year
    def get_athlete_first_year_pr(self, athlete_id, event_name):
        self._start_connection()
        if self._get_units(event_name) == 'dist':
            order = 'DESC'
        else:
            order = 'ASC'
        pr1= self.curr.execute("""SELECT min, sec_or_meters, year
                                    FROM Performances
                                    WHERE athlete_id= ? AND event_name = ?
                                    ORDER BY year asc, min, sec_or_meters ?
                                    LIMIT 1""",(
                                    athlete_id, event_name, order
                                    ))
        pr1= pr1.fetchall()
        self._close_connection()
        return pr1
#Returns selected athletes slowest time/distance in first year. (Used for first year imp)
    def get_athlete_first_year_slowest(self, athlete_id, event_name):
        self._start_connection()
        if self._get_units(event_name) == 'dist':
            order = 'ASC'
        else:
            order = 'DESC'
        slowest = self.curr.execute("""SELECT min, sec_or_meters
                                        FROM Performances
                                        WHERE athlete_id = ? AND event_name = ?
                                        ORDER BY year asc, min, sec_or_meters ?
                                        LIMIT 1""",(
                                        athlete_id, event_name, order
                                        ))
        slowest=slowest.fetchall()
        self._close_connection()
        return slowest
"""
#Returns selected athletes overall improvment
    def get_athlete_overall_imp(self):
        self._start_connection()

        overallImp=


        overallImp =overallImp.fetchall()
        self._close_connection()
        return overall

#Returns selected athletes improvement in first year
    def get_athlete_first_year_imp(self):
        self._start_connection()

        year1Imp=

        year1Imp= year1Imp.fetchall()
        self._close_connection()
        return year1Imp"""

def _get_units(self, event_name):
        self._start_connection()
        self.curr.execute("""SELECT DISTINCT time_or_dist FROM Performances
                                WHERE event_name = ?""", (event_name
                                ))
        units = units.fetchall()
        units = units[0][0]
        self._close_connection()
        return units
