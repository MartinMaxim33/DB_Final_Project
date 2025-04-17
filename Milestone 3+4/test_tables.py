# Script to let us test the functionality of the courses table.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

def list_player():
    cur.execute("SELECT * FROM player")
    rows = cur.fetchall()
    print("Here are the players:\n")
    print(f"{'Name':<20} {'Hometown':<15} {'Age':<5} {'Height':<7} {'Weight':<7} {'School':<30}")
    print("-" * 90)
    for player in rows:
        full_name = f"{player['first_name']} {player['last_name']}"
        print(f"{full_name:<20} {player['hometown']:<15} {player['age']:<5} {player['height']:<7} {player['weight']:<7} {player['school']:<30}")

def list_championships():
    cur.execute("SELECT * FROM championships")
    rows = cur.fetchall()
    print("Here are the championship records:")
    for champ in rows:
        print(f"{champ['year']} {champ['league']} Championship:")
        print(f"  Name: {champ['name']}")
        print(f"  Winner Team ID: {champ['winner']}")
        print(f"  Loser Team ID: {champ['loser']}")
        print(f"  Score: {champ['score']}")
        print(f"  MVP Player ID: {champ['mvp']}")
        print("-" * 40)

def list_teams():
    cur.execute("SELECT * FROM Teams")
    rows = cur.fetchall()
    print("Here are the teams:")
    for team in rows:
        print(f"Team Name: {team['t_name']}, City: {team['city']}, State: {team['state']}, League: {team['league']}")

def list_venues():
    cur.execute("SELECT * FROM Venues")
    rows = cur.fetchall()
    print("Here are the venues:")
    for venue in rows:
        print(f"Venue Name: {venue['name']}, City: {venue['city']}, Type: {venue['type']}, Capacity: {venue['capacity']}")

def list_games():
    cur.execute("SELECT g.date, g.time, t1.t_name AS team1, t2.t_name AS team2, g.score, v.name AS venue FROM Games g \
                 JOIN Teams t1 ON g.team1 = t1.team_id \
                 JOIN Teams t2 ON g.team2 = t2.team_id \
                 JOIN Venues v ON g.venue = v.name")
    rows = cur.fetchall()
    print("Here are the games:")
    for game in rows:
        print(f"Date: {game['date']}, Time: {game['time']}, {game['team1']} vs {game['team2']}, Score: {game['score']}, Venue: {game['venue']}")

def list_leagues():
    cur.execute("SELECT * FROM Leagues")
    rows = cur.fetchall()
    print("Here are the leagues:")
    for league in rows:
        print(f"League Name: {league['name']}, Commissioner: {league['commissioner']}, Net Worth: ${league['net_worth']}")

def main():
    list_player()
    list_championships()
    list_teams()
    list_venues()
    list_games()
    list_leagues()
    ##delete_all_courses()
    ##add_courses_from_csv("courses.csv")
    ##list_player()


main()
cur.close()
conn.close()