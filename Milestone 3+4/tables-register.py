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

@ui.page('/nhl')
def nhl_page():
    ui.label("NHL Home Page")

@ui.page('/nba')
def nba_page():
    ui.label("NBA Home Page")

@ui.page('/mlb')
def mlb_page():
    ui.label("MLB Home Page")

ui.run(reload=False)