from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from WhereDoIHaveAnAccount.scraper import scrape

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:63342",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# get list of accounts from a user
# take email, password and imap-server as input
# return list of accounts
@app.get("/accounts/")
async def get_accounts(email: str, password: str, imap_server: str):
    return scrape(email, password, imap_server)