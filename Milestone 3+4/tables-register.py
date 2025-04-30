import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui
from collections import Counter

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
    ui.link("Dashboard", "/dashboard")

@ui.page('/nfl')
def nfl_page():
    ui.label("NFL Home Page")
    ui.link("Teams", "/nfl/teams")
    ui.link("Players", "/nfl/players")
    ui.link("Games", "/nfl/games")
    ui.link("Standings", "/nfl/standings")
    ui.link("Back to Home", "/")

@ui.page('/nhl')
def nhl_page():
    ui.label("NHL Home Page")
    ui.link("Teams", "/nhl/teams")
    ui.link("Players", "/nhl/players")
    ui.link("Games", "/nhl/games")
    ui.link("Standings", "/nhl/standings")
    ui.link("Back to Home", "/")

@ui.page('/nba')
def nba_page():
    ui.label("NBA Home Page")
    ui.link("Teams", "/nba/teams")
    ui.link("Players", "/nba/players")
    ui.link("Games", "/nba/games")
    ui.link("Standings", "/nba/standings")
    ui.link("Back to Home", "/")

@ui.page('/mlb')
def mlb_page():
    ui.label("MLB Home Page")
    ui.link("Teams", "/mlb/teams")
    ui.link("Players", "/mlb/players")
    ui.link("Games", "/mlb/games")
    ui.link("Standings", "/mlb/standings")
    ui.link("Back to Home", "/")

def get_mlb_players_ages():
    cur.execute("select age from player natural join teams where league='MLB'")
    rows = cur.fetchall()
    return rows
def get_nhl_players_ages():
    cur.execute("select age from player natural join teams where league='NHL'")
    rows = cur.fetchall()
    return rows
def get_nfl_players_ages():
    cur.execute("select age from player natural join teams where league='NFL'")
    rows = cur.fetchall()
    return rows
def get_nba_players_ages():
    cur.execute("select age from player natural join teams where league='NBA'")
    rows = cur.fetchall()
    return rows
def get_player_ages():
    cur.execute("select age from player natural join teams")
    rows = cur.fetchall()
    return rows

def get_player_colleges():
    cur.execute("select college from player natural join teams")
    rows = cur.fetchall()
    return rows

def get_venue_capacity():
    cur.execute("select t_name, league, capacity from venues natural join teams")
    rows = cur.fetchall()
    return rows

def get_player_states():
    cur.execute("select hometown_state from player")
    rows = cur.fetchall()
    return rows


@ui.page('/dashboard')
def dashboard_page():
    ui.label("Dashboard")

    states = get_player_states()
    state_counts = Counter(row['hometown_state'] for row in states)
    state_labels = [str(state) for state in sorted(state_counts.keys())]
    player_counts = [state_counts[state] for state in sorted(state_counts.keys())]
    if not state_counts:
        ui.label("No player state data available")
    else:
        ui.echart({
            'title': {'text': 'Athletes by State'},
            'tooltip': {'trigger': 'axis'},
            'xAxis': {
                'type': 'category',
                'data': state_labels,
                'axisLabel': {'interval': 0, 'rotate': 45}  # No rotation needed for short age labels
            },
            'yAxis': {
                'type': 'value',
                'name': 'Number of Players'
            },
            'series': [{
                'data': player_counts,
                'type': 'bar',
                'name': 'Players',
                'itemStyle': {
                    'color': '#3398DB'  # Blue color from example
                }
            }]
        })


    mlb_ages = get_mlb_players_ages()
    nfl_ages = get_nfl_players_ages()
    nba_ages = get_nba_players_ages()
    nhl_ages = get_nhl_players_ages()
    age_counts = Counter(row['age'] for row in mlb_ages)
    nfl_counts = Counter(row['age'] for row in nfl_ages)
    nba_counts = Counter(row['age'] for row in nba_ages)
    nhl_counts = Counter(row['age'] for row in nhl_ages)
    ui.label(f"Age counts: {age_counts}")
    ui.label(f"NFL counts: {nfl_counts}")
    ui.label(f"NBA counts: {nba_counts}")
    ui.label(f"NHL counts: {nhl_counts}")
    age_labels = [str(age) for age in sorted(age_counts.keys())]
    nfl_labels = [str(age) for age in sorted(nfl_counts.keys())]
    nhl_labels = [str(age) for age in sorted(nhl_counts.keys())]
    nba_labels = [str(age) for age in sorted(nba_counts.keys())]
    player_counts = [age_counts[age] for age in sorted(age_counts.keys())]
    nfl_player_counts = [nfl_counts[age] for age in sorted(nfl_counts.keys())]
    nhl_player_counts = [nhl_counts[age] for age in sorted(nhl_counts.keys())]
    nba_player_counts = [nba_counts[age] for age in sorted(nba_counts.keys())]


    # Create bar chart
    if not age_counts:
        ui.label("No player age data available")
    else:
        ui.echart({
            'title': {'text': 'MLB Players by Age'},
            'tooltip': {'trigger': 'axis'},
            'xAxis': {
                'type': 'category',
                'data': age_labels,
                'axisLabel': {'interval': 0, 'rotate': 0}
            },
            'yAxis': {
                'type': 'value',
                'name': 'Number of Players'
            },
            'series': [{
                'data': player_counts,
                'type': 'bar',
                'name': 'Players',
                'itemStyle': {
                    'color': '#3398DB'
                }
            }]
        })
    if not nfl_counts:
        ui.label("No player age data available")
    else:
        ui.echart({
            'title': {'text': 'NFL Players by Age'},
            'tooltip': {'trigger': 'axis'},
            'xAxis': {
                'type': 'category',
                'data': nfl_labels,
                'axisLabel': {'interval': 0, 'rotate': 0}
            },
            'yAxis': {
                'type': 'value',
                'name': 'Number of Players'
            },
            'series': [{
                'data': nfl_player_counts,
                'type': 'bar',
                'name': 'Players',
                'itemStyle': {
                    'color': '#3398DB'
                }
            }]
        })

    if not nba_counts:
        ui.label("No player age data available")
    else:
        ui.echart({
            'title': {'text': 'NBA Players by Age'},
            'tooltip': {'trigger': 'axis'},
            'xAxis': {
                'type': 'category',
                'data': nba_labels,
                'axisLabel': {'interval': 0, 'rotate': 0}
            },
            'yAxis': {
                'type': 'value',
                'name': 'Number of Players'
            },
            'series': [{
                'data': nba_player_counts,
                'type': 'bar',
                'name': 'Players',
                'itemStyle': {
                    'color': '#3398DB'
                }
            }]
        })
    if not nhl_labels:
        ui.label("No player age data available")
    else:
        ui.echart({
            'title': {'text': 'NHL Players by Age'},
            'tooltip': {'trigger': 'axis'},
            'xAxis': {
                'type': 'category',
                'data': nhl_labels,
                'axisLabel': {'interval': 0, 'rotate': 0}
            },
            'yAxis': {
                'type': 'value',
                'name': 'Number of Players'
            },
            'series': [{
                'data': nhl_player_counts,
                'type': 'bar',
                'name': 'Players',
                'itemStyle': {
                    'color': '#3398DB'
                }
            }]
        })
    # All leagues chart
    all_ages = get_player_ages()  # No league filter
    all_age_counts = Counter(row['age'] for row in all_ages)
    all_age_labels = [str(age) for age in sorted(all_age_counts.keys())]
    all_player_counts = [all_age_counts[age] for age in sorted(all_age_counts.keys())]

    if not all_age_counts:
        ui.label("No player age data available (all leagues)")
    else:
        ui.echart({
            'title': {'text': 'Players by Age (All Leagues)'},
            'tooltip': {'trigger': 'axis'},
            'xAxis': {
                'type': 'category',
                'data': all_age_labels,
                'axisLabel': {'interval': 0, 'rotate': 0}
            },
            'yAxis': {
                'type': 'value',
                'name': 'Number of Players'
            },
            'series': [{
                'data': all_player_counts,
                'type': 'bar',
                'name': 'Players',
                'itemStyle': {'color': '#3398DB'}
            }]
        })

    colleges = get_player_colleges()
    college_counts = Counter(row['college'] for row in colleges if row['college'] and row['college'] != 'None')
    pie_data = [
        {
            'name': college,
            'value': count,
            'itemStyle': {
                'color': '#000000' if college == 'USC' else '#9B1B30' if college == 'Alabama' else None
            }
        }
        for college, count in sorted(college_counts.items())
    ]

    if not college_counts:
        ui.label("No player college data available")
    else:
        ui.echart({
            'title': {
                'text': 'Players by College (All Leagues)',
                'left': 'center'
            },
            'tooltip': {
                'trigger': 'item'
            },
            'legend': {
                'orient': 'vertical',
                'left': 'left'
            },
            'series': [{
                'name': 'College',
                'type': 'pie',
                'radius': '50%',
                'data': pie_data,
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        })

    venues = get_venue_capacity()
    league_capacities = {}
    for row in venues:
        league = row['league']
        capacity = row['capacity']
        if league and capacity:  # Skip None or zero capacities
            league_capacities[league] = league_capacities.get(league, 0) + capacity
    capacity_data = [
        {'name': league, 'value': total}
        for league, total in sorted(league_capacities.items(), key=lambda x: x[1], reverse=True)  # Sort by capacity
    ]

    if not capacity_data:
        ui.label("No venue capacity data available")
    else:
        ui.echart({
            'title': {
                'text': 'Total Stadium Capacity by League',
                'left': 'center'
            },
            'tooltip': {
                'trigger': 'item'
            },
            'legend': {
                'orient': 'vertical',
                'left': 'left'
            },
            'series': [{
                'name': 'League',
                'type': 'pie',
                'radius': '50%',
                'data': capacity_data,
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        })

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

@ui.page('/nfl/standings')
def nfl_standings_page():
    ui.label("NFL Standings")
    ui.link("Back to NFL", "/nfl")
    standings_rows = get_nfl_standings()
    standings_table = ui.table(rows=standings_rows)

@ui.page('/nhl/standings')
def nhl_standings_page():
    ui.label("NHL Standings")
    ui.link("Back to NHL", "/nhl")
    standings_rows = get_nhl_standings()
    standings_table = ui.table(rows=standings_rows)

@ui.page('/nba/standings')
def nba_standings_page():   
    ui.label("NBA Standings")
    ui.link("Back to NBA", "/nba")
    standings_rows = get_nba_standings()
    standings_table = ui.table(rows=standings_rows)

@ui.page('/mlb/standings')
def mlb_standings_page():
    ui.label("MLB Standings")
    ui.link("Back to MLB", "/mlb")
    standings_rows = get_mlb_standings()
    standings_table = ui.table(rows=standings_rows)

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
            schedule = get_team_schedule('NFL',team_name)
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
            schedule = get_team_schedule('NHL',team_name)
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
            schedule = get_team_schedule('MLB',team_name)
            ui.table(rows=schedule)

def get_nfl_standings():
    cur.execute("""
        WITH wins AS (
            SELECT winner AS team, COUNT(*) AS wins
            FROM games
            WHERE league = 'NFL'
            GROUP BY winner
        ),
        losses AS (
            SELECT loser AS team, COUNT(*) AS losses
            FROM games
            WHERE league = 'NFL'
            GROUP BY loser
        ),
        combined AS (
            SELECT
                COALESCE(wins.team, losses.team) AS team,
                COALESCE(wins.wins, 0) AS wins,
                COALESCE(losses.losses, 0) AS losses
            FROM wins
            LEFT JOIN losses ON wins.team = losses.team
            UNION
            SELECT
                COALESCE(wins.team, losses.team) AS team,
                COALESCE(wins.wins, 0) AS wins,
                COALESCE(losses.losses, 0) AS losses
            FROM losses
            LEFT JOIN wins ON wins.team = losses.team
        )
        SELECT
            ROW_NUMBER() OVER (ORDER BY wins DESC) AS rank,
            team,
            wins,
            losses
        FROM combined
        ORDER BY wins DESC
    """)
    return cur.fetchall()

def get_nhl_standings():
    cur.execute("""
        WITH wins AS (
            SELECT winner AS team, COUNT(*) AS wins
            FROM games
            WHERE league = 'NHL'
            GROUP BY winner
        ),
        losses AS (
            SELECT loser AS team, COUNT(*) AS losses
            FROM games
            WHERE league = 'NHL'
            GROUP BY loser
        ),
        combined AS (
            SELECT
                COALESCE(wins.team, losses.team) AS team,
                COALESCE(wins.wins, 0) AS wins,
                COALESCE(losses.losses, 0) AS losses
            FROM wins
            LEFT JOIN losses ON wins.team = losses.team
            UNION
            SELECT
                COALESCE(wins.team, losses.team) AS team,
                COALESCE(wins.wins, 0) AS wins,
                COALESCE(losses.losses, 0) AS losses
            FROM losses
            LEFT JOIN wins ON wins.team = losses.team
        )
        SELECT
            ROW_NUMBER() OVER (ORDER BY wins DESC) AS rank,
            team,
            wins,
            losses
        FROM combined
        ORDER BY wins DESC
    """)
    return cur.fetchall()

def get_nba_standings():
    cur.execute("""
        WITH wins AS (
            SELECT winner AS team, COUNT(*) AS wins
            FROM games
            WHERE league = 'NBA'
            GROUP BY winner
        ),
        losses AS (
            SELECT loser AS team, COUNT(*) AS losses
            FROM games
            WHERE league = 'NBA'
            GROUP BY loser
        ),
        combined AS (
            SELECT
                COALESCE(wins.team, losses.team) AS team,
                COALESCE(wins.wins, 0) AS wins,
                COALESCE(losses.losses, 0) AS losses
            FROM wins
            LEFT JOIN losses ON wins.team = losses.team
            UNION
            SELECT
                COALESCE(wins.team, losses.team) AS team,
                COALESCE(wins.wins, 0) AS wins,
                COALESCE(losses.losses, 0) AS losses
            FROM losses
            LEFT JOIN wins ON wins.team = losses.team
        )
        SELECT
            ROW_NUMBER() OVER (ORDER BY wins DESC) AS rank,
            team,
            wins,
            losses
        FROM combined
        ORDER BY wins DESC
    """)
    return cur.fetchall()

def get_mlb_standings():
    cur.execute("""
        WITH wins AS (
            SELECT winner AS team, COUNT(*) AS wins
            FROM games
            WHERE league = 'MLB'
            GROUP BY winner
        ),
        losses AS (
            SELECT loser AS team, COUNT(*) AS losses
            FROM games
            WHERE league = 'MLB'
            GROUP BY loser
        ),
        combined AS (
            SELECT
                COALESCE(wins.team, losses.team) AS team,
                COALESCE(wins.wins, 0) AS wins,
                COALESCE(losses.losses, 0) AS losses
            FROM wins
            LEFT JOIN losses ON wins.team = losses.team
            UNION
            SELECT
                COALESCE(wins.team, losses.team) AS team,
                COALESCE(wins.wins, 0) AS wins,
                COALESCE(losses.losses, 0) AS losses
            FROM losses
            LEFT JOIN wins ON wins.team = losses.team
        )
        SELECT
            ROW_NUMBER() OVER (ORDER BY wins DESC) AS rank,
            team,
            wins,
            losses
        FROM combined
        ORDER BY wins DESC
    """)
    return cur.fetchall()


def get_team_roster(league, team_name):
    cur.execute("""
        SELECT first_name, last_name, jersey, age, height, weight, college, hometown, hometown_state
        FROM player 
        NATURAL JOIN teams 
        WHERE league = %s AND t_name = %s
    """, (league, team_name))
    return cur.fetchall()

def get_team_schedule(league_name, team_name):
    cur.execute("""
        SELECT distinct 
            team1,
            team2,
            winner, 
            loser,
            date,
            time,
            venue
        FROM games 
        NATURAL JOIN venues
        WHERE league = %s AND (team1 = %s OR team2 = %s)
        ORDER BY date, time
    """, (league_name, team_name, team_name))
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

def get_nfl_players():
    cur.execute("select first_name, last_name, t_name, jersey, hometown, hometown_state, age, height, weight, college from player natural join teams where league='NFL'")
    rows = cur.fetchall()
    return rows

def get_nhl_players():
    cur.execute("select first_name, last_name, jersey, hometown, hometown_state, age, height, weight, college from player natural join teams where league='NHL'")
    rows = cur.fetchall()
    return rows

def get_nba_players():
    cur.execute("select first_name, last_name, jersey, hometown, hometown_state, age, height, weight, college from player natural join teams where league='NBA'")
    rows = cur.fetchall()
    return rows

def get_mlb_players():
    cur.execute("select first_name, last_name, jersey, hometown, hometown_state, age, height, weight, college from player natural join teams where league='MLB'")
    rows = cur.fetchall()
    return rows

def get_nfl_games():
    cur.execute("""
            SELECT distinct date, time, team1, team2, winner, loser, score, league FROM games natural join venues
            where league='NFL'
        """)
    rows = cur.fetchall()
    return rows

def get_nhl_games():
    cur.execute("""
        SELECT distinct date, time, team1, team2, winner, loser, score, league FROM games natural join venues
        where league = 'NHL'
    """)
    rows = cur.fetchall()
    return rows

def get_nba_games():
    cur.execute("""
            SELECT distinct date, time, team1, team2, winner, loser, score, league FROM games natural join venues
            where league = 'NBA'
        """)
    rows = cur.fetchall()
    return rows

def get_mlb_games():
    cur.execute("""
            SELECT distinct date, time, team1, team2, winner, loser, score, league FROM games natural join venues
            where league = 'MLB'
        """)
    rows = cur.fetchall()
    return rows


ui.run(reload=False)