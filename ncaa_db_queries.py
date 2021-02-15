# ncaa_db_queries
# queries for getting information from the database

import sqlite3

class DB:

    def __init__(self, name = "mockNCAA.db"):
        self.name = name

    def _start_connection(self):
        self.conn = sqlite3.connect(self.name)
        self.curr = self.conn.cursor()

    def _close_connection(self):
        self.conn.close()

    def get_div_teams(self, division, gender):
        """ returns a list of teams in a particular division and gender
            input: integer value of 1,2, or 3
            output: list of strings
        """
        self._start_connection()
        teams = self.curr.execute("""SELECTname
                                    FROM Colleges
                                    WHERE division = ? AND gender = ?""",
                                    (division, gender))
        teams = teams.fetchall()
        self._close_connection()
        return self._tuplist_to_list(teams)

    def get_team_id(self, teamName, gender):
        """ Method for getting a team id
            input: teamName(string) gender(string)
            output: team_id(int)
        """
        self._start_connection()
        team_id = self.curr.execute("""SELECT college_id
                                        FROM Colleges
                                        WHERE name = ? AND gender = ?""",
                                        (teamName, gender))
        id = team_id.fetchall()[0][0]
        self._close_connection()
        return id

    def get_team_roster(self, team_id):
        self._start_connection()
        roster = curr.execute("""SELECT name, id
                                FROM Athletes
                                WHERE college_id = ?""",
                                 (team_id,))
        roster = roster.fetchall()
        self._close_connection()
        return roster

    def get_athlete_easons(self, athlete_id):
        pass

    def get_athlete_season_events(self, athlete_id)
        pass

    def _tuplist_to_list(self, tuplist):
        return [item for tup in tuplist for item in tup]
