import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui
from nicegui.events import ValueChangeEventArguments

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

#Sort types and active query. Sort1 is the column to sort by, and sort2 is the order of sorting.
# league is the current league
sort1 = None
sort2 = None
#player_sort_query = "SELECT * FROM player natural join teams where league="

#Show user the sort type when they change it in the dropdown
def show_sort(event: ValueChangeEventArguments):
    ui.notify(f'New Sort: {event.value}')

#Get the sort type from the dropdown and build the appropriate query
def query_builder(league: str, sort1, sort2):
    if sort1 and sort2 is not None:
        if sort1 == 'First Name':
            sort1 = 'first_name'
        elif sort1 == 'Last Name':
            sort1 = 'last_name'
        elif sort1 == 'Hometown':
            sort1 = 'hometown'
        elif sort1 == 'Age':
            sort1 = 'age'
        elif sort1 == 'Height':
            sort1 = 'height'
        elif sort1 == 'Weight':
            sort1 = 'weight'
        elif sort1 == 'School':
            sort1 = 'school'
        elif sort1 == 'Jersey Number':
            sort1 = 'jerseyno'
        elif sort1 == 'Contract Amount':
            sort1 = 'contract_amt'
        elif sort1 == 'Contract Length':
            sort1 = 'contract_l'
        if sort2 == 'Ascending':
            sort2 = 'ASC'
        elif sort2 == 'Descending':
            sort2 = 'DESC'
        return f"SELECT * FROM player natural join teams where league=" + league + "ORDER BY {" +sort1 + "} {" + "sort2" + "}"
    else:
        return "No sort selected"

# Update the sort type when the dropdown value changes
def update_sort(league, event: ValueChangeEventArguments, sort1: str, sort2: str):
    new_query = query_builder(league, sort1, sort2)  # Rebuild the query
    refresh_player_list(new_query)  # Refresh the displayed data

# Refresh the displayed player list
def refresh_player_list(new_query):
    cur.execute(new_query)
    rows = cur.fetchall()
    print("Here are the players:\n")
    print(f"{'Name':<20} {'Hometown':<15} {'Age':<5} {'Height':<7} {'Weight':<7} {'School':<30} {'Jersey Number':<5} {'Contract Amount':<15} {'Contract Length':<15}")
    print("-" * 90)
    for player in rows:
        full_name = f"{player['first_name']} {player['last_name']}"
        print(f"{full_name:<20} {player['hometown']:<15} {player['age']:<5} {player['height']:<7} {player['weight']:<7} {player['school']:<30} {player['jersey_number']:<5} {player['contract_amount']:<15} {player['contract_length']:<15}")

# List all players with dropdowns for sorting
def list_all_players(league):
    with ui.row:
        ui.select(['First Name', 'Last Name', 'Hometown', 'Age', 'Height', 'Weight', 'School', 'Jersey Number', 'Contract Amount', 'Contract Length'],
                  on_change=lambda e: update_sort(e, 'sort1')).bind_value(sort1, 'value')
        ui.select(['Ascending', 'Descending'],
                  on_change=lambda e: update_sort(e, 'sort2')).bind_value(sort2, 'value')
    update_sort(league, sort1, sort2)

def main():
    list_all_players()


main()
cur.close()
conn.close()