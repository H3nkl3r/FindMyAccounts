import eel
import WhereDoIHaveAnAccount.scraper


@eel.expose
def expose_scrape(username, password, imap_server):
    domains = WhereDoIHaveAnAccount.scraper.scrape(username, password, imap_server)
    return list(domains)

def main():
    # Set web files folder
    eel.init('gui/web')
    eel.start(page='index.html')

