import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui

# Database connection setup - simple approach for a databases class
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")
cur = conn.cursor(row_factory=dict_row)


# Database access functions
def get_teams(league):
    """Get teams for a specific league"""
    cur.execute("SELECT t_name FROM teams WHERE league=%s ORDER BY t_name", (league,))
    return cur.fetchall()


def get_players(league):
    """Get players for a specific league"""
    cur.execute("""
        SELECT first_name, last_name, t_name, jerseyno, hometown, age, 
               height, weight, hand, school 
        FROM player NATURAL JOIN teams 
        WHERE league=%s
        ORDER BY t_name, last_name, first_name
    """, (league,))
    return cur.fetchall()


def get_games(league):
    """Get games for a specific league"""
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
        WHERE t1.league = %s AND t2.league = %s
        ORDER BY date DESC, time DESC
    """, (league, league))
    return cur.fetchall()


def get_team_roster(league, team_name):
    """Get roster for a specific team"""
    cur.execute("""
        SELECT first_name, last_name, jerseyno, age, height, weight, school 
        FROM player 
        NATURAL JOIN teams 
        WHERE league = %s AND t_name = %s
        ORDER BY jerseyno
    """, (league, team_name))
    return cur.fetchall()


def get_team_schedule(league, team_name):
    """Get schedule for a specific team"""
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
        LEFT JOIN teams AS tw ON games.winner = tw.team_id
        WHERE (t1.t_name = %s OR t2.t_name = %s)
        AND t1.league = %s
        ORDER BY date, time
    """, (team_name, team_name, team_name, team_name, team_name, league))
    return cur.fetchall()


# UI Components
def create_header():
    """Create a consistent header/navigation bar"""
    with ui.header().classes('bg-blue-800 text-white p-4'):
        with ui.row().classes('w-full items-center'):
            ui.label('Sports Statistics').classes('text-2xl font-bold mr-8')

            with ui.row().classes('gap-4'):
                ui.link('Home', '/').classes('text-blue-200')
                ui.link('NFL', '/nfl').classes('text-blue-200')
                ui.link('NHL', '/nhl').classes('text-blue-200')
                ui.link('NBA', '/nba').classes('text-blue-200')
                ui.link('MLB', '/mlb').classes('text-blue-200')
                ui.link('Fantasy', '/fantasy').classes('text-blue-200')
                ui.link('Dashboard', '/dashboard').classes('text-blue-200')


# Page Definitions
@ui.page('/')
def homepage():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("Welcome to the Sports Statistics Portal").classes('text-2xl font-bold mb-4')

        with ui.grid(columns=2).classes('gap-4 mt-4'):
            for league in ['NFL', 'NHL', 'NBA', 'MLB']:
                with ui.card().classes('p-4 bg-blue-50'):
                    ui.label(league).classes('text-xl font-bold')
                    ui.link(f"View {league}", f'/{league.lower()}').classes('text-blue-600')


@ui.page('/nfl')
def nfl_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("NFL Home Page").classes('text-2xl font-bold mb-4')

        with ui.row().classes('gap-4 mb-4'):
            ui.link("Teams", "/nfl/teams").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Players", "/nfl/players").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Games", "/nfl/games").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Back to Home", "/").classes('px-4 py-2 bg-gray-600 text-white rounded')


@ui.page('/nhl')
def nhl_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("NHL Home Page").classes('text-2xl font-bold mb-4')

        with ui.row().classes('gap-4 mb-4'):
            ui.link("Teams", "/nhl/teams").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Players", "/nhl/players").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Games", "/nhl/games").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Back to Home", "/").classes('px-4 py-2 bg-gray-600 text-white rounded')


@ui.page('/nba')
def nba_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("NBA Home Page").classes('text-2xl font-bold mb-4')

        with ui.row().classes('gap-4 mb-4'):
            ui.link("Teams", "/nba/teams").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Players", "/nba/players").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Games", "/nba/games").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Back to Home", "/").classes('px-4 py-2 bg-gray-600 text-white rounded')


@ui.page('/mlb')
def mlb_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("MLB Home Page").classes('text-2xl font-bold mb-4')

        with ui.row().classes('gap-4 mb-4'):
            ui.link("Teams", "/mlb/teams").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Players", "/mlb/players").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Games", "/mlb/games").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Back to Home", "/").classes('px-4 py-2 bg-gray-600 text-white rounded')


@ui.page('/dashboard')
def dashboard_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("Dashboard").classes('text-2xl font-bold mb-4')
        ui.link("Back to Home", "/").classes('px-4 py-2 bg-gray-600 text-white rounded')


# Players Pages
@ui.page('/nfl/players')
def nfl_players_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("NFL Players").classes('text-2xl font-bold mb-4')
        ui.link("Back to NFL", "/nfl").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        nfl_players_rows = get_players('NFL')
        ui.table(rows=nfl_players_rows).classes('w-full')


@ui.page('/nhl/players')
def nhl_players_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("NHL Players").classes('text-2xl font-bold mb-4')
        ui.link("Back to NHL", "/nhl").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        nhl_players_rows = get_players('NHL')
        ui.table(rows=nhl_players_rows).classes('w-full')


@ui.page('/nba/players')
def nba_players_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("NBA Players").classes('text-2xl font-bold mb-4')
        ui.link("Back to NBA", "/nba").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        nba_players_rows = get_players('NBA')
        ui.table(rows=nba_players_rows).classes('w-full')


@ui.page('/mlb/players')
def mlb_players_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("MLB Players").classes('text-2xl font-bold mb-4')
        ui.link("Back to MLB", "/mlb").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        mlb_players_rows = get_players('MLB')
        ui.table(rows=mlb_players_rows).classes('w-full')


# Teams Pages
@ui.page('/nfl/teams')
def nfl_teams_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("NFL Teams").classes('text-2xl font-bold mb-4')
        ui.link("Back to NFL", "/nfl").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        nfl_teams_rows = get_teams('NFL')
        with ui.grid(columns=3).classes('gap-4'):
            for team in nfl_teams_rows:
                with ui.card().classes('p-4 bg-blue-50'):
                    ui.link(team['t_name'], f"/nfl/team/{team['t_name']}").classes('text-blue-700 font-bold')


@ui.page('/nhl/teams')
def nhl_teams_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("NHL Teams").classes('text-2xl font-bold mb-4')
        ui.link("Back to NHL", "/nhl").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        nhl_teams_rows = get_teams('NHL')
        with ui.grid(columns=3).classes('gap-4'):
            for team in nhl_teams_rows:
                with ui.card().classes('p-4 bg-blue-50'):
                    ui.link(team['t_name'], f"/nhl/team/{team['t_name']}").classes('text-blue-700 font-bold')


@ui.page('/nba/teams')
def nba_teams_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("NBA Teams").classes('text-2xl font-bold mb-4')
        ui.link("Back to NBA", "/nba").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        nba_teams_rows = get_teams('NBA')
        with ui.grid(columns=3).classes('gap-4'):
            for team in nba_teams_rows:
                with ui.card().classes('p-4 bg-blue-50'):
                    ui.link(team['t_name'], f"/nba/team/{team['t_name']}").classes('text-blue-700 font-bold')


@ui.page('/mlb/teams')
def mlb_teams_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("MLB Teams").classes('text-2xl font-bold mb-4')
        ui.link("Back to MLB", "/mlb").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        mlb_teams_rows = get_teams('MLB')
        with ui.grid(columns=3).classes('gap-4'):
            for team in mlb_teams_rows:
                with ui.card().classes('p-4 bg-blue-50'):
                    ui.link(team['t_name'], f"/mlb/team/{team['t_name']}").classes('text-blue-700 font-bold')


# Team Detail Pages
@ui.page('/nfl/team/{team_name}')
def nfl_team_page(team_name: str):
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label(f"{team_name} Team Page").classes('text-2xl font-bold mb-4')
        ui.link("Back to NFL Teams", "/nfl/teams").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        with ui.tabs().classes('w-full') as tabs:
            roster_tab = ui.tab('Roster')
            schedule_tab = ui.tab('Schedule')

        with ui.tab_panels(tabs, value=roster_tab).classes('w-full'):
            with ui.tab_panel(roster_tab):
                ui.label("Team Roster").classes('text-xl font-bold mt-4 mb-2')
                roster = get_team_roster('NFL', team_name)
                ui.table(rows=roster).classes('w-full')

            with ui.tab_panel(schedule_tab):
                ui.label("Team Schedule").classes('text-xl font-bold mt-4 mb-2')
                schedule = get_team_schedule('NFL', team_name)
                ui.table(rows=schedule).classes('w-full')


@ui.page('/nhl/team/{team_name}')
def nhl_team_page(team_name: str):
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label(f"{team_name} Team Page").classes('text-2xl font-bold mb-4')
        ui.link("Back to NHL Teams", "/nhl/teams").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        with ui.tabs().classes('w-full') as tabs:
            roster_tab = ui.tab('Roster')
            schedule_tab = ui.tab('Schedule')

        with ui.tab_panels(tabs, value=roster_tab).classes('w-full'):
            with ui.tab_panel(roster_tab):
                ui.label("Team Roster").classes('text-xl font-bold mt-4 mb-2')
                roster = get_team_roster('NHL', team_name)
                ui.table(rows=roster).classes('w-full')

            with ui.tab_panel(schedule_tab):
                ui.label("Team Schedule").classes('text-xl font-bold mt-4 mb-2')
                schedule = get_team_schedule('NHL', team_name)
                ui.table(rows=schedule).classes('w-full')


@ui.page('/nba/team/{team_name}')
def nba_team_page(team_name: str):
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label(f"{team_name} Team Page").classes('text-2xl font-bold mb-4')
        ui.link("Back to NBA Teams", "/nba/teams").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        with ui.tabs().classes('w-full') as tabs:
            roster_tab = ui.tab('Roster')
            schedule_tab = ui.tab('Schedule')

        with ui.tab_panels(tabs, value=roster_tab).classes('w-full'):
            with ui.tab_panel(roster_tab):
                ui.label("Team Roster").classes('text-xl font-bold mt-4 mb-2')
                roster = get_team_roster('NBA', team_name)
                ui.table(rows=roster).classes('w-full')

            with ui.tab_panel(schedule_tab):
                ui.label("Team Schedule").classes('text-xl font-bold mt-4 mb-2')
                schedule = get_team_schedule('NBA', team_name)
                ui.table(rows=schedule).classes('w-full')


@ui.page('/mlb/team/{team_name}')
def mlb_team_page(team_name: str):
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label(f"{team_name} Team Page").classes('text-2xl font-bold mb-4')
        ui.link("Back to MLB Teams", "/mlb/teams").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        with ui.tabs().classes('w-full') as tabs:
            roster_tab = ui.tab('Roster')
            schedule_tab = ui.tab('Schedule')

        with ui.tab_panels(tabs, value=roster_tab).classes('w-full'):
            with ui.tab_panel(roster_tab):
                ui.label("Team Roster").classes('text-xl font-bold mt-4 mb-2')
                roster = get_team_roster('MLB', team_name)
                ui.table(rows=roster).classes('w-full')

            with ui.tab_panel(schedule_tab):
                ui.label("Team Schedule").classes('text-xl font-bold mt-4 mb-2')
                schedule = get_team_schedule('MLB', team_name)
                ui.table(rows=schedule).classes('w-full')


# Games Pages
@ui.page('/nfl/games')
def nfl_games_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("NFL Games").classes('text-2xl font-bold mb-4')
        ui.link("Back to NFL", "/nfl").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        nfl_games_rows = get_games('NFL')
        ui.table(rows=nfl_games_rows).classes('w-full')


@ui.page('/nhl/games')
def nhl_games_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("NHL Games").classes('text-2xl font-bold mb-4')
        ui.link("Back to NHL", "/nhl").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        nhl_games_rows = get_games('NHL')
        ui.table(rows=nhl_games_rows).classes('w-full')


@ui.page('/nba/games')
def nba_games_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("NBA Games").classes('text-2xl font-bold mb-4')
        ui.link("Back to NBA", "/nba").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        nba_games_rows = get_games('NBA')
        ui.table(rows=nba_games_rows).classes('w-full')


@ui.page('/mlb/games')
def mlb_games_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("MLB Games").classes('text-2xl font-bold mb-4')
        ui.link("Back to MLB", "/mlb").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')

        mlb_games_rows = get_games('MLB')
        ui.table(rows=mlb_games_rows).classes('w-full')


# Fantasy Pages
@ui.page('/fantasy')
def fantasy_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("Fantasy Home Page").classes('text-2xl font-bold mb-4')

        with ui.row().classes('gap-4 mb-4'):
            ui.link("Players to Draft", "/fantasy/players").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("My Team", "/fantasy/team").classes('px-4 py-2 bg-blue-600 text-white rounded')
            ui.link("Back to Home", "/").classes('px-4 py-2 bg-gray-600 text-white rounded')


@ui.page('/fantasy/players')
def fantasy_players_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("Fantasy Players").classes('text-2xl font-bold mb-4')
        ui.link("Back to Fantasy", "/fantasy").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')


@ui.page('/fantasy/team')
def fantasy_team_page():
    create_header()

    with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
        ui.label("Fantasy Team").classes('text-2xl font-bold mb-4')
        ui.link("Back to Fantasy", "/fantasy").classes('px-4 py-2 bg-gray-600 text-white rounded mb-4')


# Add a simple footer to all pages
@ui.page('*')
def add_footer():
    with ui.footer().classes('bg-gray-800 text-white p-4 mt-8'):
        ui.label('© 2025 Sports Statistics Portal').classes('text-sm')


# Run the application
ui.run(reload=False)