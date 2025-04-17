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

def add_courses_from_csv(filename):
    with open(filename, 'r') as file:
        with cur.copy(f"COPY courses FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

def delete_all_players():
    cur.execute("DELETE FROM player")  # careful! deletes everything.
    conn.commit()

def main():
    list_player()
    list_championships()
    ##delete_all_courses()
    ##add_courses_from_csv("courses.csv")
    ##list_player()


main()
cur.close()
conn.close()