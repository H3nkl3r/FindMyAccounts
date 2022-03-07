import os
from collections import Set
from functools import partialmethod

from tqdm import tqdm

from WhereDoIHaveAnAccount.scraper import scrape

TEST_EMAIl_USERNAME = os.environ.get('TEST_EMAIL_USERNAME')
TEST_EMAIL_PASSWORD = os.environ.get('TEST_EMAIL_PASSWORD')
TEST_EMAIL_IMAP_SERVER = os.environ.get('TEST_EMAIL_IMAP_SERVER')


def test_scrape():
    tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)
    domains = scrape(TEST_EMAIl_USERNAME, TEST_EMAIL_PASSWORD, TEST_EMAIL_IMAP_SERVER)
    assert isinstance(domains, Set)
    assert len(domains) is not 0
