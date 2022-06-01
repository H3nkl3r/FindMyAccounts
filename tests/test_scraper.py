# Copyright (c) 2022 Timo Kühne
import os
import sys
import pytest

from FindMyAccounts.scraper import distinct_scrape, get_email_headers, sklearn_scrape, filtered_scrape, \
    get_domain_from_email

TEST_EMAIl_USERNAME = os.environ['TEST_EMAIL_USERNAME']
TEST_EMAIL_PASSWORD = os.environ['TEST_EMAIL_PASSWORD']
TEST_EMAIL_IMAP_SERVER = os.environ['TEST_EMAIL_IMAP_SERVER']


def test_scrape():
    domains = distinct_scrape(TEST_EMAIl_USERNAME, TEST_EMAIL_PASSWORD, TEST_EMAIL_IMAP_SERVER)
    assert isinstance(domains, list)
    assert len(domains) is not 0


def test_get_email_headers_email_not_valid_error():
    response = get_email_headers('not_valid_email@email', 'TEST_EMAIL_PASSWORD', 'TEST_EMAIL_IMAP_SERVER')
    assert response == 'email is not valid'


def test_get_email_header_login_error():
    response = get_email_headers(TEST_EMAIl_USERNAME, 'wrong_password', TEST_EMAIL_IMAP_SERVER)
    assert response == 'Authentication failed: If you have 2-Factor-Authentication activated for your Email, ' \
                       'you need to use an App-Password '


@pytest.mark.skipif(sys.version_info <= (3, 10), reason='the generated pickle files are very sensitive to different '
                                                        'versions of sklearn with which the model was exported')
def test_sklearn_scrape():
    domains = sklearn_scrape(TEST_EMAIl_USERNAME, TEST_EMAIL_PASSWORD, TEST_EMAIL_IMAP_SERVER, 'tests/dump_model.pkl',
                             'tests/dump_vectorizer.pkl')
    assert isinstance(domains, list)
    assert len(domains) is not 0


def test_filtered_scrape():
    domains = filtered_scrape(TEST_EMAIl_USERNAME, TEST_EMAIL_PASSWORD, TEST_EMAIL_IMAP_SERVER,
                              'tests/dump_filter_list.feather')
    assert isinstance(domains, list)
    assert len(domains) is not 0


def test_filtered_scrape_error():
    domains = filtered_scrape('TEST_EMAIl_USERNAME', 'TEST_EMAIL_PASSWORD', 'TEST_EMAIL_IMAP_SERVER',
                              'tests/dump_filter_list_error.feather')
    assert isinstance(domains, str)


def test_sklearn_scrape_error():
    domains = sklearn_scrape('TEST_EMAIl_USERNAME', 'TEST_EMAIL_PASSWORD', 'TEST_EMAIL_IMAP_SERVER',
                             'tests/dump_model_error.pkl', 'tests/dump_vectorizer_error.pkl')
    assert isinstance(domains, str)


def test_distinct_scrape_error():
    domains = distinct_scrape('TEST_EMAIl_USERNAME', 'TEST_EMAIL_PASSWORD', 'TEST_EMAIL_IMAP_SERVER')
    assert isinstance(domains, str)


def test_domain_from_email_value_error():
    domain = get_domain_from_email('')
    assert domain is None


def test_get_email_header_error():
    response = get_email_headers(TEST_EMAIl_USERNAME, 'TEST_EMAIL_PASSWORD', 'TEST_EMAIL_IMAP_SERVER')
    assert response == 'An internal error has occurred!'

