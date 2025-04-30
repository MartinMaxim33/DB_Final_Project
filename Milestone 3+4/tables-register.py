import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui
from collections import Counter
from psycopg import errors

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

# Global variable for dark mode
dark_mode_enabled = False

# Function to load dark mode state (use the global variable)
def load_dark_mode():
    ui.dark_mode(dark_mode_enabled)

# Function to toggle dark mode (updates the global variable)
def toggle_dark_mode():
    global dark_mode_enabled
    dark_mode_enabled = not dark_mode_enabled
    ui.dark_mode(dark_mode_enabled)

# Page setup— called on each page load to capture dark mode
def page_setup():
    load_dark_mode()

@ui.page('/')
def homepage():
        # Navbar
        with ui.header().classes('bg-gradient-to-r from-slate-900 to-blue-600 text-white shadow-lg'):
            ui.label("🏈 SportsDB").classes('text-2xl font-bold px-4')
            ui.space()
            ui.link("Home", "/").classes('text-white hover:underline px-3')

        with ui.column().classes('items-center text-center mt-10'):
            ui.label("Your Gateway to All Major Sports").classes('text-4xl font-bold text-gray-900 dark:text-white')
            ui.label("Live Scores. Fantasy Stats. Deep Analytics.").classes('text-lg text-gray-500 dark:text-gray-400')

        # Leagues
        leagues = [
            {'name': 'NFL', 'url': '/nfl',
             'img': 'https://upload.wikimedia.org/wikipedia/en/a/a2/National_Football_League_logo.svg'},
            {'name': 'NBA', 'url': '/nba',
             'img': 'https://upload.wikimedia.org/wikipedia/en/0/03/National_Basketball_Association_logo.svg'},
            {'name': 'MLB', 'url': '/mlb',
             'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Major_League_Baseball_logo.svg/1200px-Major_League_Baseball_logo.svg.png'},
            {'name': 'NHL', 'url': '/nhl', 'img': 'https://upload.wikimedia.org/wikipedia/en/3/3a/05_NHL_Shield.svg'},
            {'name': 'Filtering', 'url': '/filtering', 'img': 'https://static.nike.com/a/images/f_auto/dpr_3.0,cs_srgb/w_363,c_limit/19b8a89a-afe7-4db0-ba6a-2bb50df14b6f/what-are-the-positions-in-american-football.jpg'},
            {'name': 'Dashboard', 'url': '/dashboard',
             'img': 'https://images.ctfassets.net/pdf29us7flmy/2wG8ah2H71AaboKXxJikkC/76e80c9d3833d1054bc327db256e69a0/GOLD-6487-CareerGuide-Batch04-Images-GraphCharts-02-Bar.png'},
        ]

        with ui.grid(columns=3).classes('gap-6 p-8 max-w-full mx-auto'):  # Use max-w-full to take the entire width
            for league in leagues:
                with ui.link().props(f'href={league["url"]}').classes(
                        'w-full'):  # Use .props() to set the href attribute
                    with ui.card().classes(
                            'hover:scale-105 hover:shadow-2xl transition-transform duration-300 cursor-pointer p-4 w-full'):  # Cards take full width of their column
                        ui.image(league['img']).classes('w-full h-48 object-contain mb-2')
                        ui.label(league['name']).classes('text-xl font-semibold text-center')

        # Footer
        with ui.footer().classes(
                'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
            ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
            ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
                'Toggle Dark Mode')

@ui.page('/nfl')
def nfl_page():
    ui.label("NFL Home Page")
    ui.link("Teams", "/nfl/teams")
    ui.link("Players", "/nfl/players")
    ui.link("Games", "/nfl/games")
    ui.link("Standings", "/nfl/standings")
    ui.link("Championships", "/nfl/championships")
    ui.link("Back to Home", "/")

@ui.page('/nhl')
def nhl_page():
    ui.label("NHL Home Page")
    ui.link("Teams", "/nhl/teams")
    ui.link("Players", "/nhl/players")
    ui.link("Games", "/nhl/games")
    ui.link("Standings", "/nhl/standings")
    ui.link("Championships", "/nhl/championships")
    ui.link("Back to Home", "/")

@ui.page('/nba')
def nba_page():
    ui.label("NBA Home Page")
    ui.link("Teams", "/nba/teams")
    ui.link("Players", "/nba/players")
    ui.link("Games", "/nba/games")
    ui.link("Standings", "/nba/standings")
    ui.link("Championships", "/nba/championships")
    ui.link("Back to Home", "/")

@ui.page('/mlb')
def mlb_page():
    ui.label("MLB Home Page")
    ui.link("Teams", "/mlb/teams")
    ui.link("Players", "/mlb/players")
    ui.link("Games", "/mlb/games")
    ui.link("Standings", "/mlb/standings")
    ui.link("Championships", "/mlb/championships")
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

def get_teams_by_state(state):
    try:
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT team_name FROM team WHERE state = %s", (state,))
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"Error fetching teams for state {state}: {e}")
        return []

# Database functions
def get_player_states():
    cur.execute("select hometown_state from player")
    rows = cur.fetchall()
    return rows

def get_players_by_state(state):
    try:
        conn.rollback()  # Clear transaction issues
        cur.execute("SELECT name FROM player WHERE hometown_state = %s", (state,))
        rows = cur.fetchall()
        conn.commit()
        return rows
    except (errors.OperationalError, errors.ProgrammingError) as e:
        print(f"Error fetching players for state {state}: {e}")
        conn.rollback()
        return []

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

def get_team_states():
    try:
        conn.rollback()
        cur.execute("SELECT DISTINCT state FROM teams WHERE state IS NOT NULL AND state != '' ORDER BY state")
        rows = cur.fetchall()
        conn.commit()
        return [row['state'] for row in rows]
    except (errors.OperationalError, errors.ProgrammingError) as e:
        print(f"Error fetching team states: {e}")
        conn.rollback()
        return []

def get_teams_by_state(state):
    try:
        conn.rollback()
        cur.execute("SELECT t_name FROM teams WHERE state = %s", (state,))
        rows = cur.fetchall()
        conn.commit()
        return rows
    except (errors.OperationalError, errors.ProgrammingError) as e:
        print(f"Error fetching teams for state {state}: {e}")
        conn.rollback()
        return []

# Filtering page (updated to filter teams)
@ui.page('/filtering')
def filtering_page():
    conn.rollback()
    ui.label("Team Filtering by State")

    state_options = get_team_states()
    if not state_options:
        ui.label("No states available")
    else:
        # Create table (initially empty)
        team_table = ui.table(
            columns=[{'name': 't_name', 'label': 'Team Name', 'field': 't_name'}],
            rows=[],
            row_key='t_name'
        )

        def update_team_table(state):
            # Fetch real team data
            teams = get_teams_by_state(state)
            team_table.rows = [{'t_name': row['t_name']} for row in teams]
            team_table.update()
            ui.notify(f"{'No teams found' if not teams else f'Showing {len(teams)} team(s)'} in {state}")

        # Dropdown
        ui.label("Select a State")
        ui.select(
            options=state_options,
            label="Select State",
            value=state_options[0] if state_options else None,
            on_change=lambda e: update_team_table(e.value)
        )

        # Initialize table with default state
        if state_options:
            update_team_table(state_options[0])

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
    with ui.grid(columns=6).classes('w-full'):
        for team in nfl_teams_rows:
            ui.link(team['t_name'], f"/nfl/team/{team['t_name']}")
    
    ui.link("Back to NFL Teams", "/nfl")

@ui.page('/nhl/teams')
def nhl_teams_page():
    ui.label("NHL Teams")
    nhl_teams_rows = get_nhl_teams()
    with ui.grid(columns=6).classes('w-full'):
        for team in nhl_teams_rows:
            ui.link(team['t_name'], f"/nhl/team/{team['t_name']}")

    ui.link("Back to NHL Teams", "/nhl")

@ui.page('/nba/teams')
def nba_teams_page():   
    ui.label("NBA Teams")
    nba_teams_rows = get_nba_teams()
    with ui.grid(columns=6).classes('w-full'):
        for team in nba_teams_rows:
            ui.link(team['t_name'], f"/nba/team/{team['t_name']}")

    ui.link("Back to NBA Teams", "/nba")

@ui.page('/mlb/teams')
def mlb_teams_page():
    ui.label("MLB Teams")
    mlb_teams_rows = get_mlb_teams()
    with ui.grid(columns=6).classes('w-full'):
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

@ui.page('/nhl/championships')
def nhl_championships_page():
    ui.label("NHL Championships")
    ui.link("Back to NHL","/nhl")
    nhl_champ_rows = get_nhl_champs()
    championships_table = ui.table(rows=nhl_champ_rows)

@ui.page('/nba/championships')
def nba_championships_page():
    ui.label("NBA Championships")
    ui.link("Back to NBA", "/nba")
    nba_champ_rows = get_nba_champs()
    championships_table = ui.table(rows=nba_champ_rows)

@ui.page('/mlb/championships')
def mlb_championships_page():
    ui.label("MLB Championships")
    ui.link("Back to MLB", "/mlb")
    mlb_champ_rows = get_mlb_champs()
    championships_table = ui.table(rows=mlb_champ_rows)

@ui.page('/nfl/championships')
def nfl_championships_page():
    ui.label("NFL Championships")
    ui.link("Back to NFL", "/nfl")
    nfl_champ_rows = get_nfl_champs()
    championships_table = ui.table(rows=nfl_champ_rows)


@ui.page('/nfl/team/{team_name}')
def nfl_team_page(team_name: str):
    ui.label(f"{team_name} Team Page")
    
    ui.link("Back to NFL Teams", "/nfl/teams")
    
    with ui.tabs().classes('w-full') as tabs:
        roster_tab = ui.tab('Roster')
        schedule_tab = ui.tab('Schedule')
        about_tab = ui.tab('About')

    with ui.tab_panels(tabs, value=roster_tab).classes('w-full'):
        with ui.tab_panel(roster_tab):
            ui.label("Team Roster")
            roster = get_team_roster('NFL', team_name)
            ui.table(rows=roster)
            
        with ui.tab_panel(schedule_tab):
            ui.label("Team Schedule")
            schedule = get_team_schedule('NFL',team_name)
            ui.table(rows=schedule)
        with ui.tab_panel(about_tab):
            ui.label("About")
            about = get_team_coach('NFL',team_name)
            about2 = get_team_champs('NFL',team_name)
            ui.table(rows=about)
            ui.table(rows=about2)

@ui.page('/nhl/team/{team_name}')
def nhl_team_page(team_name: str):
    ui.label(f"{team_name} Team Page")
    
    ui.link("Back to NHL Teams", "/nhl/teams")
    
    with ui.tabs().classes('w-full') as tabs:
        roster_tab = ui.tab('Roster')
        schedule_tab = ui.tab('Schedule')
        about_tab = ui.tab('About')

    with ui.tab_panels(tabs, value=roster_tab).classes('w-full'):
        with ui.tab_panel(roster_tab):
            ui.label("Team Roster")
            roster = get_team_roster('NHL', team_name)
            ui.table(rows=roster)
            
        with ui.tab_panel(schedule_tab):
            ui.label("Team Schedule")
            schedule = get_team_schedule('NHL',team_name)
            ui.table(rows=schedule)

        with ui.tab_panel(about_tab):
            ui.label("About")
            about = get_team_coach('NHL',team_name)
            ui.table(rows=about)
            about2 = get_team_champs('NHL',team_name)
            ui.table(rows=about2)


@ui.page('/nba/team/{team_name}')
def nba_team_page(team_name: str):
    ui.label(f"{team_name} Team Page")
    
    ui.link("Back to NBA Teams", "/nba/teams")
    
    with ui.tabs().classes('w-full') as tabs:
        roster_tab = ui.tab('Roster')
        schedule_tab = ui.tab('Schedule')
        about_tab = ui.tab('About')

    with ui.tab_panels(tabs, value=roster_tab).classes('w-full'):
        with ui.tab_panel(roster_tab):
            ui.label("Team Roster")
            roster = get_team_roster('NBA', team_name)
            ui.table(rows=roster)
            
        with ui.tab_panel(schedule_tab):
            ui.label("Team Schedule")
            schedule = get_team_schedule('NBA', team_name)
            ui.table(rows=schedule)
        with ui.tab_panel(about_tab):
            ui.label("About")
            about = get_team_coach('NBA',team_name)
            ui.table(rows=about)
            about2 = get_team_champs('NBA',team_name)
            ui.table(rows=about2)

@ui.page('/mlb/team/{team_name}')
def mlb_team_page(team_name: str):
    ui.label(f"{team_name} Team Page")
    
    ui.link("Back to MLB Teams", "/mlb/teams")
    
    with ui.tabs().classes('w-full') as tabs:
        roster_tab = ui.tab('Roster')
        schedule_tab = ui.tab('Schedule')
        about_tab = ui.tab('About')

    with ui.tab_panels(tabs, value=roster_tab).classes('w-full'):
        with ui.tab_panel(roster_tab):
            ui.label("Team Roster")
            roster = get_team_roster('MLB', team_name)
            ui.table(rows=roster)
            
        with ui.tab_panel(schedule_tab):
            ui.label("Team Schedule")
            schedule = get_team_schedule('MLB',team_name)
            ui.table(rows=schedule)

        with ui.tab_panel(about_tab):
            ui.label("About")
            about = get_team_coach('MLB',team_name)
            ui.table(rows=about)
            about2 = get_team_champs('MLB',team_name)
            ui.table(rows=about2)

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
        SELECT first_name as first, last_name as last, jersey as number, age, height, weight, college, hometown, hometown_state as state
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

def get_team_coach(league_name, team_name):
    cur.execute("""select coach_name as coach, c_age as age from coach natural join teams where teams.league = %s and coach.t_name = %s""",
                (league_name, team_name))
    return cur.fetchall()
def get_team_champs(league_name, team_name):
    cur.execute("""select c.year, c.winner, c.loser, c.score, c.mvp, c.arena from champs c join teams t on c.winner = t.t_name where t.league = %s and t.t_name = %s""",
                (league_name, team_name))
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

def get_nhl_champs():
    cur.execute("select c.year, c.winner, c.loser, c.score, c.mvp, c.arena from champs c join teams t on c.winner = t.t_name where t.league = 'NFL'")
    get_nhl_champs = cur.fetchall()
    return get_nhl_champs

def get_mlb_champs():
    cur.execute("select c.year, c.winner, c.loser, c.score, c.mvp, c.arena from champs c join teams t on c.winner = t.t_name where t.league = 'MLB'")
    get_mlb_champs = cur.fetchall()
    return get_mlb_champs

def get_nfl_champs():
    cur.execute("select c.year, c.winner, c.loser, c.score, c.mvp, c.arena from champs c join teams t on c.winner = t.t_name where t.league = 'NFL'")
    get_nfl_champs = cur.fetchall()
    return get_nfl_champs

def get_nba_champs():
    cur.execute("select c.year, c.winner, c.loser, c.score, c.mvp, c.arena from champs c join teams t on c.winner = t.t_name where t.league = 'NBA'")
    get_nba_champs = cur.fetchall()
    return get_nba_champs

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