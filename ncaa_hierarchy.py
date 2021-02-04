# ncaa_hierarchy

class Division:

    def __init__(self, name, teams = []):
        self._name = name
        self._teams = teams

    def add_team(self, team):
        self._teams.append(team)

    def get_name(self):
        return self._name

    def get_teams(self):
        return self._teams

class team:

    def __init__(self, tName, gender, athletes = []):
        self._name = tName
        self._roster = athletes
        self._gender = gender

    def add_athlete(self, athlete):
        self._athletes.append(athlete)

    def get_team_name(self):
        return self._name

    def get_team_roster(self):
        return self._roster

    def get_team_gender(self):
        return self._gender

class athlete:

    def __init__(self, name, history = {}):
        self._name = name
        self._history = history

    def add_event(self, event):
        self._history[event] = []

    def add_performance(self, event, mark, meet, date):
        self._history[event].append((mark, meet, date))

    def get_events(self):
        return self._history.keys()

    def get_event_his(self, event):
        return self._history[event]
