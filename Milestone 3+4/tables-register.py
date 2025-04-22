import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

@ui.page('/')
def homepage():
    ui.label("Welcome to the homepage!")
    ui.link("NFL", "/nfl")
    ui.link("NHL", "/nhl")
    ui.link("NBA", "/nba")
    ui.link("MLB", "/mlb")

@ui.page('/nfl')
def nfl_page():
    ui.label("NFL Home Page")
    ui.link("Players", "/nfl/players")
    ui.link("Games", "/nfl/games")

@ui.page('/nhl')
def nhl_page():
    ui.label("NHL Home Page")
    ui.link("Players", "/nhl/players")
    ui.link("Games", "/nhl/games")

@ui.page('/nba')
def nba_page():
    ui.label("NBA Home Page")
    ui.link("Players", "/nba/players")
    ui.link("Games", "/nba/games")

@ui.page('/mlb')
def mlb_page():
    ui.label("MLB Home Page")
    ui.link("Players", "/mlb/players")
    ui.link("Games", "/mlb/games")

@ui.page('/nhl/players')
def nhl_players_page():
    ui.label("NHL Players Home Page")
    nhl_players_rows = get_nhl_players()
    nhl_players_table = ui.table(rows=nhl_players_rows)

@ui.page('/nba/players')
def nba_players_page():
    ui.label("NBA Players Home Page")
    nba_players_rows = get_nba_players()
    nba_players_table = ui.table(rows=nba_players_rows)

@ui.page('/mlb/players')
def mlb_players_page():
    ui.label("MLB Players Home Page")
    mlb_players_rows = get_mlb_players()
    mlb_players_table = ui.table(rows=mlb_players_rows)

@ui.page('/nfl/players')
def nfl_players_page():
    ui.label("NFL Players Home Page")
    nfl_players_rows = get_nfl_players()
    nfl_players_table = ui.table(rows=nfl_players_rows)

@ui.page('/nhl/games')
def nhl_games_page():
    ui.label("NHL Games Home Page")
    nhl_games_rows = get_nhl_games()
    nhl_games_table = ui.table(rows=nhl_games_rows)

@ui.page('/nba/games')
def nba_games_page():
    ui.label("NBA Games Home Page")
    nba_games_rows = get_nba_games()
    nba_games_table = ui.table(rows=nba_games_rows)

@ui.page('/nfl/games')
def nfl_games_page():
    ui.label("NFL Games Home Page")
    nfl_games_rows = get_nfl_games()
    nfl_games_table = ui.table(rows=nfl_games_rows)

@ui.page('mlb/games')
def mlb_games_page():
    ui.label("MLB Games Home Page")
    mlb_games_rows = get_mlb_games()
    mlb_games_table = ui.table(rows=mlb_games_rows)


def get_nhl_players():
    cur.execute("select first_name, last_name, t_name, jerseyno, hometown, age, height, weight, hand, school from player natural join teams where league='NHL'")
    rows = cur.fetchall()
    return rows

def get_nba_players():
    cur.execute("select first_name, last_name, t_name, jerseyno, hometown, age, height, weight, hand, school from player natural join teams where league='NBA'")
    rows = cur.fetchall()
    return rows

def get_nfl_players():
    cur.execute("select first_name, last_name, t_name, jerseyno, hometown, age, height, weight, hand, school from player natural join teams where league='NFL'")
    rows = cur.fetchall()
    return rows

def get_mlb_players():
    cur.execute("select first_name, last_name, t_name, jerseyno, hometown, age, height, weight, hand, school from player natural join teams where league='MLB'")
    rows = cur.fetchall()
    return rows

def get_nhl_games():
    cur.execute("SELECT t1.t_name, t1.team_id, t2.t_name, t2.team_id, winner, score, date, time, venue FROM games JOIN teams AS t1 ON games.team1 = t1.team_id JOIN teams AS t2 ON games.team2 = t2.team_id where t1.league='NHL' and t2.league = 'NHL'")
    rows = cur.fetchall()
    return rows

def get_nba_games():
    cur.execute("SELECT t1.t_name, t1.team_id, t2.t_name, t2.team_id, winner, score, date, time, venue, t1.league, t2.league FROM games JOIN teams AS t1 ON games.team1 = t1.team_id JOIN teams AS t2 ON games.team2 = t2.team_id where t1.league='NBA' and t2.league = 'NBA'")
    rows = cur.fetchall()
    return rows

def get_nfl_games():
    cur.execute("SELECT t1.t_name, t1.team_id, t2.t_name, t2.team_id, winner, score, date, time, venue, t1.league, t2.league FROM games JOIN teams AS t1 ON games.team1 = t1.team_id JOIN teams AS t2 ON games.team2 = t2.team_id where t1.league='NFL' and t2.league = 'NFL'")
    rows = cur.fetchall()
    return rows

def get_mlb_games():
    cur.execute("SELECT t1.t_name, t1.team_id, t2.t_name, t2.team_id, winner, score, date, time, venue, t1.league, t2.league FROM games JOIN teams AS t1 ON games.team1 = t1.team_id JOIN teams AS t2 ON games.team2 = t2.team_id where t1.league='MLB' and t2.league = 'MLB'")
    rows = cur.fetchall()
    return rows

ui.run(reload=False)