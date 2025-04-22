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
    ui.link("Fantasy", "/fantasy")

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
    ui.label("NHL Players")
    nhl_players_rows = get_nhl_players()
    nhl_players_table = ui.table(rows=nhl_players_rows)

@ui.page('/nba/players')
def nba_players_page():
    ui.label("NBA Players")
    nba_players_rows = get_nba_players()
    nba_players_table = ui.table(rows=nba_players_rows)

@ui.page('/mlb/players')
def mlb_players_page():
    ui.label("MLB Players")
    mlb_players_rows = get_mlb_players()
    mlb_players_table = ui.table(rows=mlb_players_rows)

@ui.page('/nfl/players')
def nfl_players_page():
    ui.label("NFL Players")
    nfl_players_rows = get_nfl_players()
    nfl_players_table = ui.table(rows=nfl_players_rows)

def format_game_row(row):
    winner_style = 'font-bold text-green-600'
    return {'Team 1': row['team1'],
            'Team 2': row['team2'],
            'Winner': ui.html(f'<span class="{winner_style}">{row["winner"]} 🏆</span>'),
            'Score': row['score'],
            'Date': row['date'],
            'Time': row['time'],
            'Venue': row['venue']
            }

@ui.page('/nhl/games')
def nhl_games_page():
    ui.label("🏒 NHL Games")
    nhl_games_rows = get_nhl_games()
    nhl_games_table = ui.table(rows=nhl_games_rows)

@ui.page('/nba/games')
def nba_games_page():
    ui.label("NBA Games")
    nba_games_rows = get_nba_games()
    nba_games_table = ui.table(rows=nba_games_rows)

@ui.page('/nfl/games')
def nfl_games_page():
    ui.label("NFL Games")
    nfl_games_rows = get_nfl_games()
    nfl_games_table = ui.table(rows=nfl_games_rows)

@ui.page('/mlb/games')
def mlb_games_page():
    ui.label("MLB Games")
    mlb_games_rows = get_mlb_games()
    mlb_games_table = ui.table(rows=mlb_games_rows)

@ui.page('/fantasy')
def fantasy_page():
    ui.label("Fantasy Home Page")
    ui.link("Players to Draft", "/fantasy/players")
    ui.link("My team", "/fantasy/team")

@ui.page('/fantasy/players')
def fantasy_players_page():
    ui.label("Fantasy Players")

@ui.page('/fantasy/team')
def fantasy_team_page():
    ui.label("Fantasy Team")


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
    cur.execute("""
        SELECT 
            t1.t_name AS team1,
            t2.t_name AS team2,
            tw.t_name AS winner,
            score,
            date,
            time,
            venue
        FROM games
        JOIN teams AS t1 ON games.team1 = t1.team_id
        JOIN teams AS t2 ON games.team2 = t2.team_id
        JOIN teams AS tw ON games.winner = tw.team_id
        WHERE t1.league = 'NHL' AND t2.league = 'NHL'
    """)
    rows = cur.fetchall()
    return rows


def get_nba_games():
    cur.execute("""
        SELECT 
            t1.t_name AS team1,
            t2.t_name AS team2,
            tw.t_name AS winner,
            score,
            date,
            time,
            venue
        FROM games
        JOIN teams AS t1 ON games.team1 = t1.team_id
        JOIN teams AS t2 ON games.team2 = t2.team_id
        JOIN teams AS tw ON games.winner = tw.team_id
        WHERE t1.league = 'NBA' AND t2.league = 'NBA'
    """)
    rows = cur.fetchall()
    return rows


def get_nfl_games():
    cur.execute("""
        SELECT 
            t1.t_name AS team1,
            t2.t_name AS team2,
            tw.t_name AS winner,
            score,
            date,
            time,
            venue
        FROM games
        JOIN teams AS t1 ON games.team1 = t1.team_id
        JOIN teams AS t2 ON games.team2 = t2.team_id
        JOIN teams AS tw ON games.winner = tw.team_id
        WHERE t1.league = 'NFL' AND t2.league = 'NFL'
    """)
    rows = cur.fetchall()
    return rows


def get_mlb_games():
    cur.execute("""
        SELECT 
            t1.t_name AS team1,
            t2.t_name AS team2,
            tw.t_name AS winner,
            score,
            date,
            time,
            venue
        FROM games
        JOIN teams AS t1 ON games.team1 = t1.team_id
        JOIN teams AS t2 ON games.team2 = t2.team_id
        JOIN teams AS tw ON games.winner = tw.team_id
        WHERE t1.league = 'MLB' AND t2.league = 'MLB'
    """)
    rows = cur.fetchall()
    return rows


ui.run(reload=False)