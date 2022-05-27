# Copyright (c) 2022 Timo Kühne
import os

from FindMyAccounts.scraper import distinct_scrape

TEST_EMAIl_USERNAME = os.environ['TEST_EMAIL_USERNAME']
TEST_EMAIL_PASSWORD = os.environ['TEST_EMAIL_PASSWORD']
TEST_EMAIL_IMAP_SERVER = os.environ['TEST_EMAIL_IMAP_SERVER']


def test_scrape():
    domains = distinct_scrape(TEST_EMAIl_USERNAME, TEST_EMAIL_PASSWORD, TEST_EMAIL_IMAP_SERVER)
    assert isinstance(domains, list)
    assert len(domains) is not 0
