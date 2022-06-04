# Copyright (c) 2022 Timo Kühne
import getpass
import logging

import pandas as pd

from xml.etree.ElementTree import fromstring
from email_validator import validate_email, EmailNotValidError
import requests

from FindMyAccounts.scraper import get_domain_from_email, distinct_scrape, validate_domain, DomainNotValidError
from imap_tools import MailboxLoginError


def get_imap_server(email):
    """
    Given an email address, return imap server if found
    :param email: email address
    :return: imap server address if specified in json
    """
    try:
        r = requests.get('https://autoconfig.thunderbird.net/v1.1/' + get_domain_from_email(email))
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        return None

    root = fromstring(r.content)
    for child in root[0]:
        if child.tag == 'incomingServer':
            return child[0].text


def main():
    print('\n#######################\n')

    while True:
        username = input("Enter username: ")

        email = None
        try:
            # Validate & take the normalized form of the email
            email = validate_email(username).email
            break
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            logging.warning(e)
            print('Try again')

    password = getpass.getpass("Enter password: ")

    imap_server = get_imap_server(username)

    if imap_server is None:
        while True:
            imap_server = input("Enter IMAP Server: ")
            try:
                imap_server = validate_domain(imap_server)
                break
            except DomainNotValidError as e:
                logging.warning(e)
                print('Try again')

    print('\nStart analysing your emails...\n')

    try:
        domains = pd.DataFrame.from_dict(distinct_scrape(username, password, imap_server))
    except MailboxLoginError:
        print('\nYour username or password is incorrect.\n')
        return

    if not isinstance(domains, str):
        print("\n\n List of all UNIQUE accounts:")
        print("-------------------------------")
        print(domains.to_string())
