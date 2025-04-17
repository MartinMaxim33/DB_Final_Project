from nicegui import ui, app

@ui.page('/protected')
def protected():
    username = app.storage.user.get('username', None)   # default if not logged in is None
    if username is None:
        ui.navigate.to('/login?redirect_url=/protected')
    else:
        ui.label("You are logged in as user: " + username)
        ui.label("Welcome to the protected page!")


##this is the easiest way to add login pages to any of the other pages
##just take the first if, redirect to the page you want, then leave out the else and type return