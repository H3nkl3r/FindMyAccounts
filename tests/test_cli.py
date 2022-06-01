# Copyright (c) 2022 Timo Kühne
import os

import FindMyAccounts.cli as cli


TEST_EMAIl_USERNAME = os.environ['TEST_EMAIL_USERNAME']
TEST_EMAIL_PASSWORD = os.environ['TEST_EMAIL_PASSWORD']
TEST_EMAIL_IMAP_SERVER = os.environ['TEST_EMAIL_IMAP_SERVER']


def test_get_imap_server():
    imap_server = cli.get_imap_server('test@gmail.com')
    assert imap_server == 'imap.gmail.com'


def test_commandline_script(monkeypatch):
    response = iter([TEST_EMAIl_USERNAME, TEST_EMAIL_IMAP_SERVER])
    monkeypatch.setattr('builtins.input', lambda x: next(response))
    monkeypatch.setattr('getpass.getpass', lambda x: TEST_EMAIL_PASSWORD)

    domains = cli.main()
    assert isinstance(domains, list)
    assert len(domains) is not 0


def test_commandline_script_error(monkeypatch):
    response = iter(['not_valid_email@email', 'TEST_EMAIL_IMAP_SERVER'])
    monkeypatch.setattr('builtins.input', lambda x: next(response))
    monkeypatch.setattr('getpass.getpass', lambda x: 'TEST_EMAIL_PASSWORD')

    domains = cli.main()
    assert isinstance(domains, str)

