import eel
import WhereDoIHaveAnAccount.scraper
import sys
import platform


@eel.expose
def expose_scrape(username, password, imap_server):
    domains = WhereDoIHaveAnAccount.scraper.scrape(username, password, imap_server)
    return list(domains)


def main():
    # Set web files folder
    page = 'index.html'
    eel_kwargs = dict(
        host='localhost',
        port=8080,
        size=(950, 550),
    )
    eel.init('gui/web')
    try:
        eel.start(page, **eel_kwargs)
    except EnvironmentError:
        # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
        if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
            eel.start(page, mode='edge', **eel_kwargs)
        else:
            eel.start(page, mode='default', **eel_kwargs)


