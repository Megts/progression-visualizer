#Test ncaa_db_queries

from ncaa_db_queries import DB

def main():
    db = DB('ncaa.db')
    id = 6592814
    e1 = '3000 Meters'
    s1 = 'Indoor'
    e2 = 'Javelin'
    s2 = 'Outdoor'
    print(e1,s1,db.get_athlete_pr(id,e1,s1))
    print(e1,s1,db.get_athlete_first_year_pr(id,e1,s1))
    print(e1,s1,db.get_athlete_first_performance(id,e1,s1))
    print(e1,s1,db.get_athlete_first_year_imp(id,e1,s1))
    print(e1,s1,db.get_athlete_overall_imp(id,e1,s1))
    print(e2,s2,db.get_athlete_pr(id,e2,s2))
    print(e2,s2,db.get_athlete_first_year_pr(id,e2,s2))
    print(e2,s2,db.get_athlete_first_performance(id,e2,s2))
    print(e2,s2,db.get_athlete_first_year_imp(id,e2,s2))
    print(e2,s2,db.get_athlete_overall_imp(id,e2,s2))

if __name__ == '__main__':
    main()
