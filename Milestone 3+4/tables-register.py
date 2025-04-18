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
    ui.link("NFL")
    ui.link("NHL")
    ui.link("NBA")
    ui.link("MLB")



ui.run(reload=False)