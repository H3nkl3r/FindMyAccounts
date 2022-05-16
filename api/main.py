from fastapi import FastAPI
from WhereDoIHaveAnAccount.scraper import scrape

app = FastAPI()


# get list of accounts from a user
# take email, password and imap-server as input
# return list of accounts
@app.get("/accounts/")
async def get_accounts(email: str, password: str, imap_server: str):
    return scrape(email, password, imap_server)
