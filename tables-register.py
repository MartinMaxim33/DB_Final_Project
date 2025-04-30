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
        load_dark_mode()
        # Navbar
        with ui.header().classes('bg-gradient-to-r from-slate-900 to-blue-600 text-white shadow-lg'):
            ui.label("🏈 SportsDB").classes('text-2xl font-bold px-4')
            ui.space()
            ui.link("Home", "/").classes('text-white hover:underline px-3')

        with ui.column().classes('items-center text-center mt-10'):
            ui.label("Your Gateway to All Major Sports").classes('text-4xl font-bold text-gray-900 dark:text-white')

        # Leagues
        leagues = [
            {'name': 'NFL', 'url': '/nfl',
             'img': 'https://upload.wikimedia.org/wikipedia/en/a/a2/National_Football_League_logo.svg'},
            {'name': 'NBA', 'url': '/nba',
             'img': 'https://upload.wikimedia.org/wikipedia/en/0/03/National_Basketball_Association_logo.svg'},
            {'name': 'MLB', 'url': '/mlb',
             'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Major_League_Baseball_logo.svg/1200px-Major_League_Baseball_logo.svg.png'},
            {'name': 'NHL', 'url': '/nhl', 'img': 'https://upload.wikimedia.org/wikipedia/en/3/3a/05_NHL_Shield.svg'},
            {'name': 'Filtering', 'url': '/filtering', 'img': 'https://as2.ftcdn.net/jpg/03/21/21/25/1000_F_321212541_50msOq3awKbgVjvKfRcZo6HJMFWpOwQJ.jpg'},
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
    load_dark_mode()

    # Header
    with ui.header().classes('bg-gradient-to-r from-red-700 to-yellow-600 text-white shadow-lg'):
        ui.label("🏈 NFL Central").classes('text-2xl font-bold px-4')
        ui.space()
        ui.link("Home", "/").classes('text-white hover:underline px-3')
        ui.link("Dashboard", "/dashboard").classes('text-white hover:underline px-3')
        ui.link("Fantasy", "/fantasy").classes('text-white hover:underline px-3')

    # Main Section
    with ui.column().classes('items-center text-center mt-10'):
        ui.label("Welcome to NFL Central").classes('text-4xl font-bold text-gray-900 dark:text-white')
        ui.label("Dive into Teams, Players, Games, and Standings").classes('text-lg text-gray-500 dark:text-gray-400')

    nfl_sections = [
        {"name": "Teams", "url": "/nfl/teams", "img": "https://thumbs.dreamstime.com/b/stadium-icon-simple-style-white-background-vector-illustration-83216570.jpg"},
        {"name": "Players", "url": "/nfl/players", "img": "https://img.freepik.com/premium-vector/american-football-player-silhouette-logo_39679-91.jpg"},
        {"name": "Games", "url": "/nfl/games", "img": "https://static.vecteezy.com/system/resources/previews/019/519/658/non_2x/schedule-icon-for-your-website-mobile-presentation-and-logo-design-free-vector.jpg"},
        {"name": "Standings", "url": "/nfl/standings", "img": "https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/512x512/plain/podium.png"},
    ]

    with ui.grid(columns=3).classes('gap-6 p-8 max-w-full mx-auto'):
        for section in nfl_sections:
            with ui.link().props(f'href={section["url"]}').classes('w-full'):
                with ui.card().classes(
                    'hover:scale-105 hover:shadow-2xl transition-transform duration-300 cursor-pointer p-4 w-full'):
                    ui.image(section['img']).classes('w-full h-48 object-contain mb-2')
                    ui.label(section['name']).classes('text-xl font-semibold text-center')

    with ui.row():
        ui.button('🏠 Home', on_click=lambda: ui.run_javascript('window.location.href = "/"'))

    # Footer
    with ui.footer().classes(
        'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')


@ui.page('/nhl')
def nhl_page():
    load_dark_mode()

    with ui.header().classes('bg-gradient-to-r from-blue-900 to-cyan-600 text-white shadow-lg'):
        ui.label("🏒 NHL Central").classes('text-2xl font-bold px-4')
        ui.space()
        ui.link("Home", "/").classes('text-white hover:underline px-3')
        ui.link("Dashboard", "/dashboard").classes('text-white hover:underline px-3')
        ui.link("Fantasy", "/fantasy").classes('text-white hover:underline px-3')

    with ui.column().classes('items-center text-center mt-10'):
        ui.label("Welcome to NHL Central").classes('text-4xl font-bold text-gray-900 dark:text-white')
        ui.label("Explore Teams, Players, Games, and Standings").classes('text-lg text-gray-500 dark:text-gray-400')

    nhl_sections = [
        {"name": "Teams", "url": "/nhl/teams", "img": "https://thumbs.dreamstime.com/b/stadium-icon-simple-style-white-background-vector-illustration-83216570.jpg"},
        {"name": "Players", "url": "/nhl/players", "img": "https://static.vecteezy.com/system/resources/previews/016/929/153/non_2x/hockey-player-silhouette-design-athlete-sign-and-symbol-vector.jpg"},
        {"name": "Games", "url": "/nhl/games", "img": "https://static.vecteezy.com/system/resources/previews/019/519/658/non_2x/schedule-icon-for-your-website-mobile-presentation-and-logo-design-free-vector.jpg"},
        {"name": "Standings", "url": "/nhl/standings", "img": "https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/512x512/plain/podium.png"},
    ]

    with ui.grid(columns=3).classes('gap-6 p-8 max-w-full mx-auto'):
        for section in nhl_sections:
            with ui.link().props(f'href={section["url"]}').classes('w-full'):
                with ui.card().classes(
                    'hover:scale-105 hover:shadow-2xl transition-transform duration-300 cursor-pointer p-4 w-full'):
                    ui.image(section['img']).classes('w-full h-48 object-contain mb-2')
                    ui.label(section['name']).classes('text-xl font-semibold text-center')

    with ui.row():
        ui.button('🏠 Home', on_click=lambda: ui.run_javascript('window.location.href = "/"'))

    with ui.footer().classes(
        'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip('Toggle Dark Mode')

@ui.page('/nba')
def nba_page():

    load_dark_mode()

    with ui.header().classes('bg-gradient-to-r from-indigo-900 to-purple-600 text-white shadow-lg'):
        ui.label("🏀 NBA Central").classes('text-2xl font-bold px-4')
        ui.space()
        ui.link("Home", "/").classes('text-white hover:underline px-3')
        ui.link("Dashboard", "/dashboard").classes('text-white hover:underline px-3')
        ui.link("Fantasy", "/fantasy").classes('text-white hover:underline px-3')

    with ui.column().classes('items-center text-center mt-10'):
        ui.label("Welcome to NBA Central").classes('text-4xl font-bold text-gray-900 dark:text-white')
        ui.label("Explore Teams, Players, Games, and Standings").classes('text-lg text-gray-500 dark:text-gray-400')

    nba_sections = [
        {"name": "Teams", "url": "/nba/teams", "img": "https://thumbs.dreamstime.com/b/stadium-icon-simple-style-white-background-vector-illustration-83216570.jpg"},
        {"name": "Players", "url": "/nba/players", "img": "https://www.creativefabrica.com/wp-content/uploads/2019/10/24/basketball-player-silhoutte-with-the-ball-logo-2-1-580x386.jpg"},
        {"name": "Games", "url": "/nba/games", "img": "https://static.vecteezy.com/system/resources/previews/019/519/658/non_2x/schedule-icon-for-your-website-mobile-presentation-and-logo-design-free-vector.jpg"},
        {"name": "Standings", "url": "/nba/standings", "img": "https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/512x512/plain/podium.png"},
    ]

    with ui.grid(columns=3).classes('gap-6 p-8 max-w-full mx-auto'):
        for section in nba_sections:
            with ui.link().props(f'href={section["url"]}').classes('w-full'):
                with ui.card().classes(
                    'hover:scale-105 hover:shadow-2xl transition-transform duration-300 cursor-pointer p-4 w-full'):
                    ui.image(section['img']).classes('w-full h-48 object-contain mb-2')
                    ui.label(section['name']).classes('text-xl font-semibold text-center')

    with ui.row():
        ui.button('🏠 Home', on_click=lambda: ui.run_javascript('window.location.href = "/"'))

    with ui.footer().classes(
        'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip('Toggle Dark Mode')

@ui.page('/mlb')
def mlb_page():

    load_dark_mode()

    with ui.header().classes('bg-gradient-to-r from-rose-700 to-red-500 text-white shadow-lg'):
        ui.label("⚾ MLB Central").classes('text-2xl font-bold px-4')
        ui.space()
        ui.link("Home", "/").classes('text-white hover:underline px-3')
        ui.link("Dashboard", "/dashboard").classes('text-white hover:underline px-3')
        ui.link("Fantasy", "/fantasy").classes('text-white hover:underline px-3')

    with ui.column().classes('items-center text-center mt-10'):
        ui.label("Welcome to MLB Central").classes('text-4xl font-bold text-gray-900 dark:text-white')
        ui.label("Explore Teams, Players, Games, and Standings").classes('text-lg text-gray-500 dark:text-gray-400')

    mlb_sections = [
        {"name": "Teams", "url": "/mlb/teams", "img": "https://thumbs.dreamstime.com/b/stadium-icon-simple-style-white-background-vector-illustration-83216570.jpg"},
        {"name": "Players", "url": "/mlb/players", "img": "https://www.shutterstock.com/image-vector/baseball-player-batter-hitter-isolated-600nw-2462157771.jpg"},
        {"name": "Games", "url": "/mlb/games", "img": "https://static.vecteezy.com/system/resources/previews/019/519/658/non_2x/schedule-icon-for-your-website-mobile-presentation-and-logo-design-free-vector.jpg"},
        {"name": "Standings", "url": "/mlb/standings", "img": "https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/512x512/plain/podium.png"},
    ]

    with ui.grid(columns=3).classes('gap-6 p-8 max-w-full mx-auto'):
        for section in mlb_sections:
            with ui.link().props(f'href={section["url"]}').classes('w-full'):
                with ui.card().classes(
                    'hover:scale-105 hover:shadow-2xl transition-transform duration-300 cursor-pointer p-4 w-full'):
                    ui.image(section['img']).classes('w-full h-48 object-contain mb-2')
                    ui.label(section['name']).classes('text-xl font-semibold text-center')

    with ui.row():
        ui.button('🏠 Home', on_click=lambda: ui.run_javascript('window.location.href = "/"'))

    with ui.footer().classes(
        'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip('Toggle Dark Mode')


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
    load_dark_mode()
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

    with ui.row():
        ui.button('🏠 Home', on_click=lambda: ui.run_javascript('window.location.href = "/"'))

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

def get_team_states():
    try:
        conn.rollback()
        cur.execute("SELECT DISTINCT state FROM teams WHERE state IS NOT NULL AND state != '' ORDER BY state")
        rows = cur.fetchall()
        conn.commit()
        return ['All States'] + [row['state'] for row in rows]
    except (errors.OperationalError, errors.ProgrammingError) as e:
        print(f"Error fetching team states: {e}")
        conn.rollback()
        return []

def get_league():
    try:
        conn.rollback()
        cur.execute("SELECT DISTINCT league FROM teams WHERE league IS NOT NULL AND league != '' ORDER BY league")
        rows = cur.fetchall()
        conn.commit()
        return ['All Leagues'] + [row['league'] for row in rows]
    except (errors.OperationalError, errors.ProgrammingError) as e:
        print(f"Error fetching leagues: {e}")
        conn.rollback()
        return []

def get_filtered_teams(state, league):
    try:
        conn.rollback()
        query = "SELECT t_name FROM teams WHERE t_name IS NOT NULL AND t_name != ''"
        params = []

        if state != 'All States':
            query += " AND state = %s"
            params.append(state)

        if league != 'All Leagues':
            query += " AND league = %s"
            params.append(league)

        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        conn.commit()
        return rows
    except (errors.OperationalError, errors.ProgrammingError) as e:
        print(f"Error fetching filtered teams: {e}")
        conn.rollback()
        return []


# Filtering page with combined filters
@ui.page('/filtering')
def filtering_page():
    load_dark_mode()
    conn.rollback()

    state_options = get_team_states()
    league_options = get_league()

    # Create a container for the dropdowns at the top
    with ui.card().classes('w-full p-4 shadow-md'):
        ui.label("Filter Teams").classes('text-xl font-bold mb-4')

        # Create a grid layout for the dropdowns
        with ui.grid(columns=2).classes('w-full gap-4'):
            # State dropdown
            with ui.column():
                ui.label("Filter by State").classes('font-medium')
                state_select = ui.select(
                    options=state_options,
                    label="Select State",
                    value=state_options[0],
                    on_change=lambda: update_team_table()
                ).classes('w-full')

            # League dropdown
            with ui.column():
                ui.label("Filter by League").classes('font-medium')
                league_select = ui.select(
                    options=league_options,
                    label="Select League",
                    value=league_options[0],
                    on_change=lambda: update_team_table()
                ).classes('w-full')

    # Create the team table below the dropdowns
    with ui.card().classes('w-full p-4 mt-4 shadow-md'):
        ui.label("Team Results").classes('text-xl font-bold mb-4')
        team_table = ui.table(
            columns=[{'name': 't_name', 'label': 'Team Name', 'field': 't_name'}],
            rows=[],
            row_key='t_name'
        ).classes('w-full')

    def update_team_table():
        state = state_select.value
        league = league_select.value
        teams = get_filtered_teams(state, league)
        team_table.rows = [{'t_name': row['t_name']} for row in teams]
        team_table.update()

        state_label = f"in {state}" if state != 'All States' else ""
        league_label = f"in {league}" if league != 'All Leagues' else ""
        filter_label = " ".join(filter(None, [state_label, league_label])).strip()

        ui.notify(f"{'No teams found' if not teams else f'Showing {len(teams)} team(s)'} {filter_label}")

    # Initialize table with default filters
    if state_options and league_options:
        update_team_table()
    else:
        ui.notify("No filter options available", type='negative')

    with ui.row():
        ui.button('🏠 Home', on_click=lambda: ui.run_javascript('window.location.href = "/"'))

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nfl/players')
def nfl_players_page():
    load_dark_mode()
    ui.label("NFL Players")
    ui.link("Back to NFL Players", "/nfl")
    nfl_players_rows = get_nfl_players()
    nfl_players_table = ui.table(rows=nfl_players_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nhl/players')
def nhl_players_page():
    load_dark_mode()
    ui.label("NHL Players")
    ui.link("Back to NHL Players", "/nhl")
    nhl_players_rows = get_nhl_players()
    nhl_players_table = ui.table(rows=nhl_players_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nba/players')
def nba_players_page():
    load_dark_mode()
    ui.label("NBA Players")
    ui.link("Back to NBA Players", "/nba")
    nba_players_rows = get_nba_players()
    nba_players_table = ui.table(rows=nba_players_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/mlb/players')
def mlb_players_page():
    load_dark_mode()
    ui.label("MLB Players")
    ui.link("Back to MLB Players", "/mlb")
    mlb_players_rows = get_mlb_players()
    mlb_players_table = ui.table(rows=mlb_players_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nfl/teams')
def nfl_teams_page():
    load_dark_mode()
    ui.label("NFL Teams")
    nfl_teams_rows = get_nfl_teams()
    with ui.grid(columns=6).classes('w-full'):
        for team in nfl_teams_rows:
            ui.link(team['t_name'], f"/nfl/team/{team['t_name']}")
    
    ui.link("Back to NFL Teams", "/nfl")

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nhl/teams')
def nhl_teams_page():
    load_dark_mode()
    ui.label("NHL Teams")
    nhl_teams_rows = get_nhl_teams()
    with ui.grid(columns=6).classes('w-full'):
        for team in nhl_teams_rows:
            ui.link(team['t_name'], f"/nhl/team/{team['t_name']}")

    ui.link("Back to NHL Teams", "/nhl")

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nba/teams')
def nba_teams_page():
    load_dark_mode()
    ui.label("NBA Teams")
    nba_teams_rows = get_nba_teams()
    with ui.grid(columns=6).classes('w-full'):
        for team in nba_teams_rows:
            ui.link(team['t_name'], f"/nba/team/{team['t_name']}")

    ui.link("Back to NBA Teams", "/nba")

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/mlb/teams')
def mlb_teams_page():
    load_dark_mode()
    ui.label("MLB Teams")
    mlb_teams_rows = get_mlb_teams()
    with ui.grid(columns=6).classes('w-full'):
        for team in mlb_teams_rows:
            ui.link(team['t_name'], f"/mlb/team/{team['t_name']}")

    ui.link("Back to MLB Teams", "/mlb")

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nfl/standings')
def nfl_standings_page():
    load_dark_mode()
    ui.label("NFL Standings")
    ui.link("Back to NFL", "/nfl")
    standings_rows = get_nfl_standings()
    standings_table = ui.table(rows=standings_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nhl/standings')
def nhl_standings_page():
    load_dark_mode()
    ui.label("NHL Standings")
    ui.link("Back to NHL", "/nhl")
    standings_rows = get_nhl_standings()
    standings_table = ui.table(rows=standings_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nba/standings')
def nba_standings_page():
    load_dark_mode()
    ui.label("NBA Standings")
    ui.link("Back to NBA", "/nba")
    standings_rows = get_nba_standings()
    standings_table = ui.table(rows=standings_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/mlb/standings')
def mlb_standings_page():
    load_dark_mode()
    ui.label("MLB Standings")
    ui.link("Back to MLB", "/mlb")
    standings_rows = get_mlb_standings()
    standings_table = ui.table(rows=standings_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nhl/championships')
def nhl_championships_page():
    load_dark_mode()
    ui.label("NHL Championships")
    ui.link("Back to NHL","/nhl")
    nhl_champ_rows = get_nhl_champs()
    championships_table = ui.table(rows=nhl_champ_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nba/championships')
def nba_championships_page():
    load_dark_mode()
    ui.label("NBA Championships")
    ui.link("Back to NBA", "/nba")
    nba_champ_rows = get_nba_champs()
    championships_table = ui.table(rows=nba_champ_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/mlb/championships')
def mlb_championships_page():
    load_dark_mode()
    ui.label("MLB Championships")
    ui.link("Back to MLB", "/mlb")
    mlb_champ_rows = get_mlb_champs()
    championships_table = ui.table(rows=mlb_champ_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nfl/championships')
def nfl_championships_page():
    load_dark_mode()
    ui.label("NFL Championships")
    ui.link("Back to NFL", "/nfl")
    nfl_champ_rows = get_nfl_champs()
    championships_table = ui.table(rows=nfl_champ_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nfl/team/{team_name}')
def nfl_team_page(team_name: str):
    load_dark_mode()
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
            ui.label("Head Coach")
            about = get_team_coach('NFL',team_name)
            ui.label("Superbowl Championships")
            about2 = get_team_champs('NFL',team_name)
            ui.table(rows=about)
            ui.table(rows=about2)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nhl/team/{team_name}')
def nhl_team_page(team_name: str):
    load_dark_mode()
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
            ui.label("Head Coach")
            about = get_team_coach('NHL',team_name)
            ui.table(rows=about)
            ui.label("Stanley Cup Championships")
            about2 = get_team_champs('NHL',team_name)
            ui.table(rows=about2)
    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nba/team/{team_name}')
def nba_team_page(team_name: str):
    load_dark_mode()
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
            ui.label("Head Coach")
            about = get_team_coach('NBA',team_name)
            ui.table(rows=about)
            ui.label("NBA Championships")
            about2 = get_team_champs('NBA',team_name)
            ui.table(rows=about2)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/mlb/team/{team_name}')
def mlb_team_page(team_name: str):
    load_dark_mode()
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
            ui.label("Head Coach")
            about = get_team_coach('MLB',team_name)
            ui.table(rows=about)
            ui.label("World Series Championships")
            about2 = get_team_champs('MLB',team_name)
            ui.table(rows=about2)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

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
    load_dark_mode()
    ui.label("NFL Games")
    ui.link("Back to NFL", "/nfl")
    nfl_games_rows = get_nfl_games()
    nfl_games_table = ui.table(rows=nfl_games_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nhl/games')
def nhl_games_page():
    load_dark_mode()
    ui.label("NHL Games")
    ui.link("Back to NHL", "/nhl")
    nhl_games_rows = get_nhl_games()
    nhl_games_table = ui.table(rows=nhl_games_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/nba/games')
def nba_games_page():
    load_dark_mode()
    ui.label("NBA Games")
    ui.link("Back to NBA", "/nba")
    nba_games_rows = get_nba_games()
    nba_games_table = ui.table(rows=nba_games_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

@ui.page('/mlb/games')
def mlb_games_page():
    load_dark_mode()
    ui.label("MLB Games")
    ui.link("Back to MLB", "/mlb")
    mlb_games_rows = get_mlb_games()
    mlb_games_table = ui.table(rows=mlb_games_rows)

    # Footer
    with ui.footer().classes(
            'mt-10 text-center text-white-400 flex justify-between items-center px-6 py-4 bg-slate-100 dark:bg-slate-800'):
        ui.label("Evan DeVine, Jud Turner, Nick Bilotti, and Martin Maxim • Built with NiceGUI").classes('text-sm')
        ui.button(icon='dark_mode', on_click=toggle_dark_mode).props('flat round dense color=primary').tooltip(
            'Toggle Dark Mode')

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