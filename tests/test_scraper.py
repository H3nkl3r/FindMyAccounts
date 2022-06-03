# Copyright (c) 2022 Timo Kühne
import os
import pytest
from FindMyAccounts.scraper import distinct_scrape, get_email_headers, get_domain_from_email, DomainNotValidError
from email_validator import EmailNotValidError
from imap_tools import MailboxLoginError

TEST_EMAIl_USERNAME = os.environ['TEST_EMAIL_USERNAME']
TEST_EMAIL_PASSWORD = os.environ['TEST_EMAIL_PASSWORD']
TEST_EMAIL_IMAP_SERVER = os.environ['TEST_EMAIL_IMAP_SERVER']


def test_scrape():
    domains = distinct_scrape(TEST_EMAIl_USERNAME, TEST_EMAIL_PASSWORD, TEST_EMAIL_IMAP_SERVER)
    assert isinstance(domains, list)
    assert len(domains) is not 0


def test_get_email_headers_email_not_valid_error():
    with pytest.raises(EmailNotValidError):
        get_email_headers('not_valid_email', TEST_EMAIL_PASSWORD, TEST_EMAIL_IMAP_SERVER)


def test_get_email_header_imap_server_not_valid_error():
    with pytest.raises(DomainNotValidError):
        get_email_headers(TEST_EMAIl_USERNAME, TEST_EMAIL_PASSWORD, 'not_valid_imap_server')


def test_get_email_header_mailbox_login_error():
    with pytest.raises(MailboxLoginError):
        get_email_headers(TEST_EMAIl_USERNAME, 'not_valid_password', TEST_EMAIL_IMAP_SERVER)


def test_domain_from_email_value_error():
    domain = get_domain_from_email('')
    assert domain is None


