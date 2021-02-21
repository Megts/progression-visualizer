# ncaa_db_queries
# queries for getting information from the database

import sqlite3

class DB:

    def __init__(self, name = "ncaa.db"):
        self.name = name
        self.sprints = ['55 Meters','60 Meters','100 Meters','200 Meters','300 Hurdles'
                        '400 Meters','55 Hurdles', '110 Hurdles', ]

    def _start_connection(self):
        try:
            self.conn = sqlite3.connect(self.name)
            self.curr = self.conn.cursor()
        except:
            print('did not connect')

    def _close_connection(self):
        self.conn.close()

    def get_div_teams(self, division, gender):
        """ returns a list of teams in a particular division and gender
            input:  division: integer value of 1,2, or 3, gender string of m or f
            output: list of strings
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
                                    ) )
        events = events.fetchall()
        self._close_connection()
        return self._tuplist_to_list(events)

    def _tuplist_to_list(self, tuplist):
        return [item for tup in tuplist for item in tup]

    def to_seconds(self,min,seconds):
        if min is not None:
            return min*60 + seconds
        return seconds

    def to_minutes(self,min,seconds):
        return min + seconds/60
