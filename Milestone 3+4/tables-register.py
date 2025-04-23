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
    ui.link("Teams", "/nfl/teams")
    ui.link("Players", "/nfl/players")
    ui.link("Games", "/nfl/games")
    ui.link("Back to Home", "/")

@ui.page('/nhl')
def nhl_page():
    ui.label("NHL Home Page")
    ui.link("Teams", "/nhl/teams")
    ui.link("Players", "/nhl/players")
    ui.link("Games", "/nhl/games")
    ui.link("Back to Home", "/")

@ui.page('/nba')
def nba_page():
    ui.label("NBA Home Page")
    ui.link("Teams", "/nba/teams")
    ui.link("Players", "/nba/players")
    ui.link("Games", "/nba/games")
    ui.link("Back to Home", "/")

@ui.page('/mlb')
def mlb_page():
    ui.label("MLB Home Page")
    ui.link("Teams", "/mlb/teams")
    ui.link("Players", "/mlb/players")
    ui.link("Games", "/mlb/games")
    ui.link("Back to Home", "/")


@ui.page('/nfl/players')
def nfl_players_page():
    ui.label("NFL Players")
    ui.link("Back to NFL Players", "/nfl")
    nfl_players_rows = get_nfl_players()
    nfl_players_table = ui.table(rows=nfl_players_rows)

@ui.page('/nhl/players')
def nhl_players_page():
    ui.label("NHL Players")
    ui.link("Back to NHL Players", "/nhl")
    nhl_players_rows = get_nhl_players()
    nhl_players_table = ui.table(rows=nhl_players_rows)

@ui.page('/nba/players')
def nba_players_page():
    ui.label("NBA Players")
    ui.link("Back to NBA Players", "/nba")
    nba_players_rows = get_nba_players()
    nba_players_table = ui.table(rows=nba_players_rows)

@ui.page('/mlb/players')
def mlb_players_page():
    ui.label("MLB Players")
    ui.link("Back to MLB Players", "/mlb")
    mlb_players_rows = get_mlb_players()
    mlb_players_table = ui.table(rows=mlb_players_rows)


@ui.page('/nfl/teams')
def nfl_teams_page():
    ui.label("NFL Teams")
    nfl_teams_rows = get_nfl_teams()
    with ui.column().classes('w-full'):
        for team in nfl_teams_rows:
            ui.link(team['t_name'], f"/nfl/team/{team['t_name']}")
    
    ui.link("Back to NFL Teams", "/nfl")

@ui.page('/nhl/teams')
def nhl_teams_page():
    ui.label("NHL Teams")
    nhl_teams_rows = get_nhl_teams()
    with ui.column().classes('w-full'):
        for team in nhl_teams_rows:
            ui.link(team['t_name'], f"/nhl/team/{team['t_name']}")

    ui.link("Back to NHL Teams", "/nhl")

@ui.page('/nba/teams')
def nba_teams_page():   
    ui.label("NBA Teams")
    nba_teams_rows = get_nba_teams()
    with ui.column().classes('w-full'):
        for team in nba_teams_rows:
            ui.link(team['t_name'], f"/nba/team/{team['t_name']}")

    ui.link("Back to NBA Teams", "/nba")

@ui.page('/mlb/teams')
def mlb_teams_page():
    ui.label("MLB Teams")
    mlb_teams_rows = get_mlb_teams()
    with ui.column().classes('w-full'):
        for team in mlb_teams_rows:
            ui.link(team['t_name'], f"/mlb/team/{team['t_name']}")

    ui.link("Back to MLB Teams", "/mlb")

@ui.page('/nfl/team/{team_name}')
def nfl_team_page(team_name: str):
    ui.label(f"{team_name} Team Page")
    
    ui.link("Back to NFL Teams", "/nfl/teams")
    
    with ui.tabs().classes('w-full') as tabs:
        roster_tab = ui.tab('Roster')
        schedule_tab = ui.tab('Schedule')
    
    with ui.tab_panels(tabs, value=roster_tab).classes('w-full'):
        with ui.tab_panel(roster_tab):
            ui.label("Team Roster")
            roster = get_team_roster('NFL', team_name)
            ui.table(rows=roster)
            
        with ui.tab_panel(schedule_tab):
            ui.label("Team Schedule")
            schedule = get_team_schedule('NFL', team_name)
            ui.table(rows=schedule)

@ui.page('/nhl/team/{team_name}')
def nhl_team_page(team_name: str):
    ui.label(f"{team_name} Team Page")
    
    ui.link("Back to NHL Teams", "/nhl/teams")
    
    with ui.tabs().classes('w-full') as tabs:
        roster_tab = ui.tab('Roster')
        schedule_tab = ui.tab('Schedule')
    
    with ui.tab_panels(tabs, value=roster_tab).classes('w-full'):
        with ui.tab_panel(roster_tab):
            ui.label("Team Roster")
            roster = get_team_roster('NHL', team_name)
            ui.table(rows=roster)
            
        with ui.tab_panel(schedule_tab):
            ui.label("Team Schedule")
            schedule = get_team_schedule('NHL', team_name)
            ui.table(rows=schedule)

@ui.page('/nba/team/{team_name}')
def nba_team_page(team_name: str):
    ui.label(f"{team_name} Team Page")
    
    ui.link("Back to NBA Teams", "/nba/teams")
    
    with ui.tabs().classes('w-full') as tabs:
        roster_tab = ui.tab('Roster')
        schedule_tab = ui.tab('Schedule')
    
    with ui.tab_panels(tabs, value=roster_tab).classes('w-full'):
        with ui.tab_panel(roster_tab):
            ui.label("Team Roster")
            roster = get_team_roster('NBA', team_name)
            ui.table(rows=roster)
            
        with ui.tab_panel(schedule_tab):
            ui.label("Team Schedule")
            schedule = get_team_schedule('NBA', team_name)
            ui.table(rows=schedule)

@ui.page('/mlb/team/{team_name}')
def mlb_team_page(team_name: str):
    ui.label(f"{team_name} Team Page")
    
    ui.link("Back to MLB Teams", "/mlb/teams")
    
    with ui.tabs().classes('w-full') as tabs:
        roster_tab = ui.tab('Roster')
        schedule_tab = ui.tab('Schedule')
    
    with ui.tab_panels(tabs, value=roster_tab).classes('w-full'):
        with ui.tab_panel(roster_tab):
            ui.label("Team Roster")
            roster = get_team_roster('MLB', team_name)
            ui.table(rows=roster)
            
        with ui.tab_panel(schedule_tab):
            ui.label("Team Schedule")
            schedule = get_team_schedule('MLB', team_name)
            ui.table(rows=schedule)

def get_team_roster(league, team_name):
    cur.execute("""
        SELECT first_name, last_name, jerseyno, age, height, weight, school 
        FROM player 
        NATURAL JOIN teams 
        WHERE league = %s AND t_name = %s
    """, (league, team_name))
    return cur.fetchall()

def get_team_schedule(league, team_name):
    cur.execute("""
        SELECT 
            date,
            time,
            venue,
            CASE 
                WHEN t1.t_name = %s THEN t2.t_name
                ELSE t1.t_name
            END AS opponent,
            CASE 
                WHEN t1.t_name = %s THEN 'Home'
                ELSE 'Away'
            END AS location,
            score,
            CASE 
                WHEN tw.t_name = %s THEN 'Win'
                WHEN score IS NULL THEN 'Upcoming'
                ELSE 'Loss'
            END AS result
        FROM games
        JOIN teams AS t1 ON games.team1 = t1.team_id
        JOIN teams AS t2 ON games.team2 = t2.team_id
        JOIN teams AS tw ON games.winner = tw.team_id
        WHERE (t1.t_name = %s OR t2.t_name = %s)
        AND t1.league = %s
        ORDER BY date, time
    """, (team_name, team_name, team_name, team_name, team_name, league))
    return cur.fetchall()


def get_nfl_teams():
    cur.execute("select t_name from teams where league='NFL'")
    get_nfl_teams = cur.fetchall()
    return get_nfl_teams

def get_nhl_teams():
    cur.execute("select t_name from teams where league='NHL'")
    get_nhl_teams = cur.fetchall()
    return get_nhl_teams

def get_nba_teams():
    cur.execute("select t_name from teams where league='NBA'")
    get_nba_teams = cur.fetchall()
    return get_nba_teams    

def get_mlb_teams():
    cur.execute("select t_name from teams where league='MLB'")
    get_mlb_teams = cur.fetchall()
    return get_mlb_teams



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

@ui.page('/nfl/games')
def nfl_games_page():
    ui.label("NFL Games")
    ui.link("Back to NFL", "/nfl")
    nfl_games_rows = get_nfl_games()
    nfl_games_table = ui.table(rows=nfl_games_rows)

@ui.page('/nhl/games')
def nhl_games_page():
    ui.label("NHL Games")
    ui.link("Back to NHL", "/nhl")
    nhl_games_rows = get_nhl_games()
    nhl_games_table = ui.table(rows=nhl_games_rows)

@ui.page('/nba/games')
def nba_games_page():
    ui.label("NBA Games")
    ui.link("Back to NBA", "/nba")
    nba_games_rows = get_nba_games()
    nba_games_table = ui.table(rows=nba_games_rows)

@ui.page('/mlb/games')
def mlb_games_page():
    ui.label("MLB Games")
    ui.link("Back to MLB", "/mlb")
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

def get_nfl_players():
    cur.execute("select first_name, last_name, t_name, jerseyno, hometown, age, height, weight, hand, school from player natural join teams where league='NFL'")
    rows = cur.fetchall()
    return rows

def get_nhl_players():
    cur.execute("select first_name, last_name, t_name, jerseyno, hometown, age, height, weight, hand, school from player natural join teams where league='NHL'")
    rows = cur.fetchall()
    return rows

def get_nba_players():
    cur.execute("select first_name, last_name, t_name, jerseyno, hometown, age, height, weight, hand, school from player natural join teams where league='NBA'")
    rows = cur.fetchall()
    return rows

def get_mlb_players():
    cur.execute("select first_name, last_name, t_name, jerseyno, hometown, age, height, weight, hand, school from player natural join teams where league='MLB'")
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